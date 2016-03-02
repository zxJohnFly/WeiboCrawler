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
        try:
            url_split = urlparse.urlparse(url).path.split('.')
            suffix = 'jpg' if len(url_split) is not 2 else url_split[-1]
            fn = os.path.join(imgfolder, filename + '_' + str(count) + '.' + suffix)

            with open(fn, 'wb') as f:
                respose = urllib2.urlopen(url)
                img = respose.read()
                f.write(img)
                f.flush()
                f.close()

            logger.info('mid: %s images downloaded' % filename)
        except Exception, e:
            logger.warning('mid: {0} error {1}'.format(filename, e))

def imgdownload(num=30):
    global imgfolder
    imgfolder = os.path.join(basepath,'img')

    if os.path.exists(imgfolder) is not True:
        os.mkdir(imgfolder)
    for con in Content.objects:
        # if con.imagesfile is True:
        #     continue
        # else:
            urls = con.images
            download(con.mid, urls)

            # con.update(imagesfile=True)


if __name__ == '__main__':
    from mongoengine import connect
    from crawler import logger
    import urllib2
    import os
    import urlparse

    basepath = '\\'.join(__file__.split('/')[0:-2])

    connect(db="Weibo")
    imgdownload()