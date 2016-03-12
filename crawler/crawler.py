from Fetcher import WeiboLogin
from Parser import InfoParser, FansParser, WeiboParser
import urllib2
import cookielib


class Parser(object):
    def __init__(self, username, password, uid):
        self.username = username
        self.password = password
        self.uid = uid

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        WeiboLogin(self.opener, self.username, self.password)

    def __loadpage(self, url, timeout=None):
        page = self.opener.open(url, timeout=timeout)

        return page.read()

    def __crawler(self, url, Parser):
        page = self.__loadpage(url)
        parser = Parser(page, self.uid)

        parser.parse()

    def weibo_link(self):
        link = 'http://weibo.com/%s?is_all=1' % self.uid
        self.__crawler(link, WeiboParser)

    def info_link(self):
        link = 'http://weibo.com/%s/info' % self.uid
        self.__crawler(link, InfoParser)

    def fans_link(self):
        link = 'http://weibo.com/%s/fans' % self.uid

        for _ in range(1,6):
            url = link + '?page=%s' % _
            self.__crawler(url, FansParser)

if __name__ == '__main__':
    from mongoengine import connect
    from setting import db_name
    connect(db=db_name)
    # uid = '5572759558'
    uid = '1661467473'

    a = Parser('2311490760@qq.com', 'zx2681618', uid)
    a.info_link()
    a.weibo_link()
    # a.weibo_link()
    # page = a.loadpage(url+uid+'?is_all=1')
    # page= a.extractor(page)

    # print page[0]
    # a.purifier(page)

