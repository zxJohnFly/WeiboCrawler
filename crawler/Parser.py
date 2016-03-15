#coding=utf-8

from bs4 import BeautifulSoup
from storage import save_uid, save_User, save_Content, save_BigV
import re
import json
import urlparse


class Parser(object):
    def purify(self, page, domid):
        soup = BeautifulSoup(page, 'lxml')
        scripts = soup.find_all('script')

        regex_script = re.compile('FM.view\((.*)\)')

        for item in scripts:
            try:
                script = regex_script.match(item.string)
            except TypeError:
                print 'TypeError: %s' % str(type(script))
                break

            if script is not None:
                script_dict = json.loads(script.group(1))

                if script_dict['domid'].startswith(domid):
                    return script_dict['html'].replace('\\r', '').replace('\\n', '').replace('\\t', '').replace('\\', '')


class InfoParser(Parser):
    def __init__(self, page, uid):
        self.page = page
        self.domid = 'Pl_Official_PersonalInfo'
        self.uid = uid

    def parse(self):
        res = self.purify(self.page, 'Pl_Official_Headerv')
        soup = BeautifulSoup(res, 'lxml')
        avt = soup.find('p', class_='photo_wrap')
        avt = avt.img['src']

        res = self.purify(self.page, self.domid)

        soup = BeautifulSoup(res, 'lxml')
        infos = soup.find('div', class_='m_wrap clearfix')

        lis = infos.find_all('li')

        name = ''
        desc = ''

        for li in lis:
            spans = li.find_all('span')

            if spans[0].string == u'昵称：':
                name = spans[1].string
            elif spans[0].string == u'简介：':
                desc = spans[1].string

        save_User(self.uid, name, avt, desc)


class FansParser(Parser):
    def __init__(self, page, uid):
        self.page = page
        self.domid = 'Pl_Official_HisRelation_'

    def parse(self):
        res = self.purify(self.page, self.domid)

        if res is None:
            return

        soup = BeautifulSoup(res, 'lxml')
        fans_info = soup.find_all('div',class_='info_connect')

        for fan in fans_info:
            span = fan.find_all('span')
            info = span[2].em.a
            uid = info['href'][3:]
            count = int(info.string)

            if count >= 100:
                print 'uid:',uid,'\t count:', count
                self.__store(uid)

    def __store(self, uid):
        save_uid(uid)


class WeiboParser(Parser):
    def __init__(self, page, uid):
        self.page = page
        self.uid = uid
        self.domid = 'Pl_Official_MyProfileFeed'

    def __formatter(self, div):
        text = ''

        for text_children in div.children:
            if text_children.__class__.__name__ is 'Tag':
                tmp = text_children.string
                if tmp is not None:
                    text += tmp
            else:
                text += text_children

        return text.strip()

    def parse(self):
        res = self.purify(self.page, self.domid)

        soup = BeautifulSoup(res, 'lxml')
        divs = soup.find_all("div", attrs={"action-type": "feed_list_item"})

        try:
            end_id = divs[0]['mid']
        except IndexError:
            raise IndexError

        for div in divs:
            weibo = div.find("div", class_="WB_feed_detail clearfix")
            WB_detail = weibo.find("div", class_="WB_detail")
            date = WB_detail.find("div", class_="WB_from S_txt2")
            date = date.a['title']

            # get content
            WB_text = WB_detail.find("div", class_="WB_text W_f14")
            text = self.__formatter(WB_text)

            # get extent content
            WB_expand = WB_detail.find("div", class_="WB_feed_expand")
            if WB_expand is not None:
                WB_expand_text = WB_expand.find("div", class_="WB_text")
                if WB_expand_text is not None:
                    expand_text = self.__formatter(WB_expand_text)
                    text = text + '::' + expand_text

            WB_media = WB_detail.find("div", class_="WB_media_wrap clearfix")
            imgs = []
            if WB_media is not None:
                # the div may contain videos and links, just ignore those
                imgs = WB_media.find_all("img")
                imgs = [img['src'] for img in imgs]

            print self.uid, 'date:',date, 'text:',text,'imgs:',imgs
            save_Content(self.uid, date, text, imgs)

class BigVParser(Parser):
    def __init__(self, page, uid):
        self.page = page
        self.uid = uid
        self.domid = 'Pl_Core_F4RightUserList'

    def parse(self):
        res = self.purify(self.page, self.domid)

        soup = BeautifulSoup(res, 'lxml')
        divs = soup.find_all("div", class_='info_name W_fb W_f14')

        for div in divs:
            a = div.a['href']
            uid = urlparse.urlparse(a).path.split('/')[-1]
            self._store(uid)


    def _store(self, uid):
        save_BigV(uid)
