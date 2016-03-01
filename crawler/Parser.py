from Fetcher import WeiboLogin
from storage import weibo_save, exist
from bs4 import BeautifulSoup
from . import Catogeries, interlude, logger
import urllib2
import urllib
import cookielib
import re
import time
import json
import socket


class MyException(Exception):
    pass


class Parser(object):
    def __init__(self, username, password, category):
        self.username = username
        self.password = password
        self.tag = category
        self.category = Catogeries[category]

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        tlogin = WeiboLogin(self.opener, self.username, self.password)
        tlogin.login()

        logger.info('crawler category: %s', self.tag)

    def __retry(self, url, times=30):
        page = None
        for _ in range(times):
            try:
                page = self.opener.open(url, timeout=60)
                page = page.read()
            except urllib2.URLError, e:
                logger.info('Fail to open "%s", try again.' % url)
            else:
                return page

    def __extractor(self, page):
        soup = BeautifulSoup(page, 'lxml')
        data = soup.find_all('script')

        regex_script = re.compile('FM.view\((.*)\)')
        regex_domid = re.compile('"domid":"Pl_Core_MixedFeed__5"')

        for item in data:
            script = regex_script.match(item.string)

            if script is not None:
                domid = regex_domid.search(script.group(1))

                if domid is not None:
                    page = script.group(1)
                    beg = page.find("html") + 7

                    return page[beg:-2]

    def __purifier(self, page):
        if page is None:
            return

        page = page.replace(r'\r', '').replace(r'\n', '').replace(r'\t', '').replace('\\', '')
        soup = BeautifulSoup(page, 'lxml')

        divs = soup.find_all("div", attrs={"action-type": "feed_list_item"})
        global end_id

        try:
            end_id = divs[0]['mid']
        except IndexError:
            raise IndexError

        for div in divs:
            mid = div['mid']

            if exist(mid):
                continue

            weibo = div.find("div", class_="WB_feed_detail clearfix")
            # get user avatar
            WB_face = weibo.find("div", class_="WB_face W_fl")
            avatar = WB_face.find("img")['src']

            WB_detail = weibo.find("div", class_="WB_detail")
            # get user name
            WB_info = WB_detail.find("div", class_="WB_info")
            name = WB_info.a.string.lstrip()

            # get content
            WB_text = WB_detail.find("div", class_="WB_text W_f14")
            text = ''
            for text_children in WB_text.children:
                if text_children.__class__.__name__ is 'Tag':
                    tmp = text_children.string
                    if tmp is not None:
                        text += tmp
                else:
                    text += text_children

            WB_media = WB_detail.find("div", class_="WB_media_wrap clearfix")
            imgs = []
            if WB_media is not None:
                # the div may contain videos and links, just ignore those
                imgs = WB_media.find_all("img")
                imgs = [img['src'] for img in imgs]

            weibo_save(name, avatar, mid, text, self.tag, imgs)
            logger.info('store mid: %s into database' % mid)

    def loadpages(self):
        page_url = 'http://d.weibo.com/{0}'.format(self.category)
        jump_url = 'http://d.weibo.com/p/aj/v6/mblog/mbloglist'

        postdata = {
            'ajwvr': '6',
            'domain': self.category,
            'from': 'faxian_hot',
            'mod': 'fenlei',
            'max_id': '',
            'filtered_min_id': '',
            'pl_name': 'Pl_Core_MixedFeed__5',
            'id': self.category,
            'script_uri': r'/' + self.category,
            'feed_type': '1',
            'tab': 'home',
            'domain_op': self.category
        }

        try:
            for iter_p in range(7):
                init_current_page = iter_p*3
                url = page_url + '?current_page={0}&since_id=&page={1}'.format(init_current_page, iter_p+1)

                logger.info('current page {0} (1/3)'.format(iter_p+1))
                page = self.__retry(url)

                if page is None:
                    raise Exception

                page = self.__extractor(page)
                self.__purifier(page)

                postdata['pre_page'] = iter_p + 1
                postdata['page'] = iter_p + 1
                postdata['end_id'] = end_id

                for _ in range(2):
                    time.sleep(interlude)

                    postdata['current_page'] = init_current_page + _ + 1
                    postdata['pagebar'] = _
                    postdata['__rnd'] = str(int(time.time()*1000))

                    pd = urllib.urlencode(postdata)
                    url = jump_url+'?'+pd
                    logger.info('current page {0} ({1}/3)'.format(iter_p+1, _+2))
                    jump = self.__retry(url)

                    if page is None:
                        raise Exception

                    jump_json = json.loads(jump)

                    self.__purifier(jump_json["data"])
        except IndexError:
            logger.info('%s Craler finished' % self.tag)
            return True
        except socket.timeout:
            return False
        except Exception, e:
            logger.debug(e)
