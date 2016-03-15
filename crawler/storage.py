#coding=utf-8
from mongoengine import Document, EmbeddedDocument, StringField, ListField, IntField,EmbeddedDocumentField,DateTimeField, BooleanField


def save_User(uid, username, avatar, desc, num):
    user = User(id=uid, username=username, avatar=avatar, description=desc, message_num=num)

    if user not in User.objects:
        user.save()
        # print 'uid: {0}\tnickname:{1}'.format(uid, username)


def save_BigV(uid):
    user = BigV(uid=uid, isCrawled=False)

    if user not in BigV.objects:
        user.save()
        print uid


def save_Content(uid, mid, datetime, text, urls):
    user = User.objects.get(id=uid)
    content = Content(mid=mid, datetime=datetime, text=text, picture_url=urls)

    if mid not in [msg.mid for msg in user.message_content]:
        user.message_content.append(content)
        user.save()


def save_uid(uid):
    _uid = Uid(uid=uid, isCrawled=False)

    if _uid not in Uid.objects:
        _uid.save()


class Content(EmbeddedDocument):
    mid = StringField(required=True, primary_key=True)
    datetime = DateTimeField(required=True)
    text = StringField()
    picture_url = ListField(StringField())


class User(Document):
    id = StringField(required=True, primary_key=True)
    username = StringField(required=True)
    avatar = StringField(required=True)
    description = StringField(required=True)
    message_num = IntField(required=True)
    message_content = ListField(EmbeddedDocumentField(Content))


class Uid(Document):
    uid = StringField(required=True, primary_key=True)
    isCrawled = BooleanField(default=False)


class BigV(Document):
    uid = StringField(required=True, primary_key=True)
    isCrawled = BooleanField(default=False)