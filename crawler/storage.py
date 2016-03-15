#coding=utf-8
from mongoengine import Document, EmbeddedDocument, StringField, ListField, IntField,EmbeddedDocumentField,DateTimeField, BooleanField


def save_User(uid, username, avatar, desc):
    user = User(id=uid, username=username, avatar=avatar, description=desc)

    if user not in User.objects:
        user.save()
        print 'uid: {0}\tnickname '


def save_BigV(uid):
    user = BigV(uid=uid, isCrawled=False)

    if user not in BigV.objects:
        user.save()
        print uid


def save_Content(uid, datetime, text, urls):
    user = User.objects.get(id=int(uid))
    content = Content(datetime=datetime, text=text, picture_url=urls)
    user.message_content.append(content)

    user.save()


def save_uid(uid):
    _uid = Uid(uid=uid, isCrawled=False)

    if _uid not in Uid.objects:
        _uid.save()


class Content(EmbeddedDocument):
    datetime = DateTimeField(required=True)
    text = StringField()
    picture_url = ListField(StringField())
    # video_url = StringField()


class User(Document):
    id = IntField(required=True, primary_key=True)
    username = StringField(required=True)
    avatar = StringField(required=True)
    description = StringField(required=True)
    # message_num = IntField()
    message_content = ListField(EmbeddedDocumentField(Content))

class Uid(Document):
    uid = StringField(required=True, primary_key=True)
    isCrawled = BooleanField(default=False)

class BigV(Document):
    uid = StringField(required=True, primary_key=True)
    isCrawled = BooleanField(default=False)
