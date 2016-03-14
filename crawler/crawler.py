from Fetcher import WeiboLogin
from Parser import InfoParser, FansParser, WeiboParser
import urllib2
import urllib
import cookielib
import time


class Crawler(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        WeiboLogin(self.opener, self.username, self.password)

    def __loadpage(self, url, timeout=None):
        page = self.opener.open(url, timeout=timeout)

        return page.read()

    def __crawler(self, url, uid, Parser):
        print url
        page = self.__loadpage(url)
        parser = Parser(page, uid)

        parser.parse()

    def weibo_link(self, uid):
        def first_block_url(page):
            return 'http://weibo.com/{0}?page={1}&is_all=1'.format(uid, page)

        def extract_block_url(page, block):
            postdata = {
            'ajwvr': '6',
            'domain': '100505',
            'pids':'',
            'profile_ftype':'1',
            'is_all':'1',
            'pagebar':str(block),
            'pl_name':'',
            'id':'100505' + str(uid),
            'script_uri': r'/u/' + str(uid),
            'feed_type':'0',
            'page': str(page),
            'pre_page': str(page),
            'domain_op':'100505',
            '__rnd':str(time.time()*1000)
            }
            postdata = urllib.urlencode(postdata)

            return 'http://weibo.com/{0}?{1}'.format(uid, postdata)

        fpage = 1
        while True:
            try:
                self.__crawler(first_block_url(fpage), uid, WeiboParser)
                self.__crawler(extract_block_url(fpage,0), uid, WeiboParser)
                self.__crawler(extract_block_url(fpage,1), uid, WeiboParser)
            except IndexError:
                break
            except Exception,e:
                print e
            fpage = fpage + 1

    def info_link(self, uid):
        link = 'http://weibo.com/%s/info' % uid
        self.__crawler(link, uid, InfoParser)

    def fans_link(self, uid):
        link = 'http://weibo.com/%s/fans' % uid

        for _ in range(1,6):
            url = link + '?page=%s' % _
            self.__crawler(url, uid, FansParser)

# if __name__ == '__main__':
#     from mongoengine import connect
#     from setting import db_name
#     connect(db=db_name)
#     uid = '5572759558'
#     # uid = '1661467473'
#
#     a = Parser('2311490760@qq.com', 'zx2681618', uid)
#     # a.info_link()
#     # a.weibo_link()
#     a.fans_link()

