from mongoengine import Document, StringField, ListField, BooleanField, ReferenceField


class User(Document):
    Name = StringField(required=True, primary_key=True)
    Avatar = StringField(required=True)


class Content(Document):
    mid = StringField(required=True, primary_key=True)
    content = StringField(required=True)
    tag = StringField(required=True)
    images = ListField()
    imagesfile = BooleanField(default=False)
    author = ReferenceField(User)


def exist(mid):
    return Content.objects(mid=str(mid)).count()


def weibo_save(name, avatar, mid, content, tag, images):
    user = User(Name=name, Avatar=avatar)
    if user not in User.objects:
        user.save()

    con = Content(mid=mid, content=content, tag=tag, author=user, images=images)
    con.save()


def download(filename, urls):
    count = 0
    for url in urls:
        count += 1
        fn = 'D:/img/'+filename + '_' + str(count) + '.' + url.split('.')[-1][0:3]
        with open(fn, 'wb') as f:
            respose = urllib2.urlopen(url)
            img = respose.read()
            f.write(img)
            f.flush()
            f.close()

def imgdownload(num=30):
    for con in Content.objects:
        urls = con.images
        download(con.mid, urls)

        # con.update(imagesfile=True)

        # con.imagesfile = True


if __name__ == '__main__':
    from mongoengine import connect
    import urllib2

    connect(db="Weibo")
    imgdownload()