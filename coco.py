from pycocotools.coco import COCO
from .db import database
from .utils import network
from . import *

net, transformer = net_init()

pre_path = '/home/wzq/coco/'
ann_file = pre_path + 'annotations/instances_train2014.json'

def build_db(db):
#    db.create_table()

    count = 0
    for tup in imgs:
        id, img = tup
	img = img.encode('utf-8')
	#exit(0)
        code, _ = network(pre_path + 'train2014/'+ img, transformer, net)
        db.insert(code48=code, img=img, label=id)
        count += 1
        if count%1000 == 0:
            db.commit()
	  #  break
    print 'build db ok, total is {}'.format(count)

cc = COCO(ann_file)

imgs = []
for id, value in cc.imgs.items():
    imgs.append((id, value['file_name']))

print 'imgs has {} imgs'.format(len(imgs))

db = database('coco')
build_db(db)
