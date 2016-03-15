from Crawler import storage, crawler
from setting import username, password

cl = crawler.Crawler(username, password)

def main():
    for uid in storage.Uid.objects:
        cl.info_link(uid.uid)
        cl.weibo_link(uid.uid)
        uid.update(isCrawled = True)

def run():
    for bigv in storage.BigV.objects:
        if not bigv.isCrawled:
            cl.fans_link(bigv.uid)
            bigv.update(isCrawled = True)

if __name__ == '__main__':
    # cl.bigV_link('1087030002_2975_2025_0')
    run()