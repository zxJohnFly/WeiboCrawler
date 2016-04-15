#coding=utf-8
from mongoengine import Document, EmbeddedDocument, StringField, ListField, IntField,EmbeddedDocumentField,DateTimeField, BooleanField
from setting import DEBUG

def save_User(uid, username, avatar, desc, num):
    if DEBUG:
        print 'uid:{0}, username:{1},avatar:{2},description:{3}'.format(uid, username, avatar, desc)
    else:
        user = User(id=uid, username=username, avatar=avatar, description=desc, message_num=num)

        if user not in User.objects:
            user.save()


def save_BigV(uid):
    user = BigV(uid=uid, isCrawled=False)

    if user not in BigV.objects:
        user.save()
        print uid


def save_Content(uid, mid, datetime, text, urls):
    if DEBUG:
        print 'uid:{0},mid:{1}'.format(uid, mid)
    else:
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

if __name__ == '__main__':
    from mongoengine import connect
    connect(db='myweibo')

    count = 0
    for user in User.objects:
        print user.id, user.message_num,'->',len(user.message_content)
        count = count + len(user.message_content)

    print count