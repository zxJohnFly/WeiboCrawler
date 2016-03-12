from mongoengine import connect
from setting import db_name

connect(db=db_name)