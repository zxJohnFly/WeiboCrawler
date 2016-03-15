from Crawler import storage, crawler
from setting import username, password
from multiprocessing import Pool

if __name__ == '__main__':
    cl = crawler.Crawler(username, password)

    for uid in storage.Uid.objects:
        if not uid.isCrawled:
            cl.crawler_pool('info_link',[uid.uid])
            cl.crawler_pool('weibo_link',[uid.uid])