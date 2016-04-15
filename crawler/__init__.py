from mongoengine import connect
from setting import DB_NAME
import logging


connect(db=DB_NAME)

logger = logging.getLogger('crawler')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('crawler.log')
fh.setLevel(logging.INFO)

fmt = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
fh.setFormatter(fmt)

logger.addHandler(fh)