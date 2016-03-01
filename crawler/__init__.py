from mongoengine import connect
import logging

logger = logging.getLogger('crawler')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)

fmt = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
ch.setFormatter(fmt)

logger.addHandler(ch)

connect(db='Weibo')

Catogeries = {
   'sport': '102803_ctg1_1388_-_ctg1_1388',
   'music': '102803_ctg1_5288_-_ctg1_5288',
   'moive': '102803_ctg1_3288_-_ctg1_3288',
   'fashion': '102803_ctg1_4488_-_ctg1_4488',
   'stars': '102803_ctg1_4288_-_ctg1_4288'
}

interlude = 5
