from Crawler import storage, crawler
from setting import username, password, thread_num
from functools import partial
#
#
# def proxy(instance, method, para):
#     instance(method, para)

if __name__ == '__main__':
    cl = crawler.Crawler(username, password)

    # func_proxy = partial(proxy,cl, 'info_link')

    # if thread_num == 1:
    #     func_proxy('1762690124')
    # else:
    #     from multiprocessing import Pool
    #
    #     p = Pool(processes=thread_num)
    #     p.map(func_proxy,['5541379719','1762690124','3514342873'])


    for uid in storage.Uid.objects[4230:]:
        if not uid.isCrawled:
            if cl.crawler_pool('info_link',[uid.uid]):
                uid.update(isCrawled=True)
                cl.crawler_pool('weibo_link',[uid.uid])
        else:
            user = storage.User.objects(uid=uid.uid)

            if user['message_num'] != len(user['message_content']):
                cl.crawler_pool('weibo_link',[uid.uid])