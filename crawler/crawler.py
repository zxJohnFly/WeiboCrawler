from Fetcher import WeiboLogin
from Parser import InfoParser, FansParser, WeiboParser, BigVParser
from . import logger
from multiprocessing import Pool
import urllib2
import urllib
import cookielib
import time
import socket
import random
import types


class Crawler(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        WeiboLogin(self.opener, self.username, self.password)

    def _get_rand(self):
        r1 = random.randint(5,10)
        r2 = random.randint(1,5)

        return r1 - r2


    def __loadpage(self, url):
        page = None

        for _ in range(5):
            try:
                page = self.opener.open(url, timeout=120)
            except socket.timeout:
                print 'timeout'
            else:
                break

        return page.read()


    def __crawler(self, url, uid, Parser):
        print url

        delay = self._get_rand()
        time.sleep(delay)

        page = self.__loadpage(url)

        if page is None:
            logger.info(url, uid)
            raise socket.timeout

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
                print 'uid:%s finished!!' % uid
                break
            except socket.timeout:
                logger.info('uid:%s timeout'%uid)
                return False
            except Exception,e:
                logger.info('uid:{0} error:'.format(uid, e))
                return False

            fpage = fpage + 1

        return True

    def info_link(self, uid):
        link = 'http://weibo.com/%s/info' % uid

        try:
            self.__crawler(link, uid, InfoParser)
        except socket.timeout:
            return False
        else:
            return True

    def fans_link(self, uid):
        link = 'http://weibo.com/%s/fans' % uid

        for _ in range(1,6):
            url = link + '?page=%s' % _
            try:
                self.__crawler(url, uid, FansParser)
            except socket.timeout:
                continue

    def bigV_link(self,category):
        for _ in range(1,141):
            url = 'http://d.weibo.com/{0}?page={1}'.format(category,_)
            self.__crawler(url,None,BigVParser)

    def crawler_pool(self, method, param):
        handle = None

        try:
            handle = self.__getattribute__(method)
        except AttributeError,e:
            print "Class crawler doesn't have method [%s]" % method
            return

        if type(param) is types.ListType:
            if len(param) == 1:
                handle(param[0])
            else:
                pass
        elif types(param) is types.StringType:
            handle(param)
        else:
            print 'inValid param'
