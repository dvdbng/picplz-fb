#!/usr/bin/env python

import urllib,json
from pyshutils import *
import fbconsole

cd("/usr/lib/picplz-fb")

fbconsole.AUTH_SCOPE = ['publish_stream',"offline_access"]
fbconsole.authenticate()
uploaded = load("picplz-uploaded",set())

data = json.loads(urllib.urlopen("http://api.picplz.com/api/v2/user.json?id=623640&include_pics=1&pic_page_size=10").read())
assert data["result"] == "ok"
photos = data["value"]["users"][0]["pics"]
photos.sort(key=lambda x:x["date"])

for img in photos:
    if img["id"] not in uploaded:
        caption = img["caption"].encode("utf-8")
        if "place" in img:
            caption = "%s (%s)" % (caption,img["place"]["name"].encode("utf-8"))

        print "uploading ", caption
        uploaded.add(img["id"])
        fi,headers = urllib.urlretrieve(img["pic_files"]["640r"]["img_url"])
        fbconsole.post('/2246799144449/photos', {
            'source':open(fi,"rb"),
            'message': "%s\n\nTaken with PicPlz http://picplz.com%s" % (caption,img["url"].encode("utf-8"))
        })

save("picplz-uploaded",uploaded)
