from Crawler import storage, crawler
from setting import username, password, process_num


def batch_uid(num):
    uids = []

    for uid in storage.Uid.objects:
        if ~uid.isCrawled:
            uids.append(uid.uid)

        if len(uid) >= num:
            break

    return uids

if __name__ == '__main__':
    nCrawler = crawler.Crawler(username, password)
    nCrawler.weibo_link(batch_uid(1)[0])

