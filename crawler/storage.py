from mongoengine import Document, StringField, ListField, ReferenceField


class User(Document):
    Name = StringField(required=True, primary_key=True)
    Avatar = StringField(required=True)


class Content(Document):
    mid = StringField(required=True, primary_key=True)
    content = StringField(required=True)
    tag = StringField(required=True)
    images = ListField()

    author = ReferenceField(User)


def exist(mid):
    return Content.objects(mid=str(mid)).count()


def weibo_save(name, avatar, mid, content, tag, images):
    user = User(Name=name, Avatar=avatar)
    if user not in User.objects:
        user.save()

    con = Content(mid=mid, content=content, tag=tag, author=user, images=images)
    con.save()