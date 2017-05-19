from pycocotools.coco import COCO
from .db import database
from .utils import network
from . import net, transformer

pre_path = '/home/wzq/coco/'
ann_file = pre_path + 'annotations/instances_val2014.json'

def build_db(db):
    db.create_table()

    count = 0
    for tup in imgs:
        id, img = tup
        code, _ = network(pre_path + 'test2014/'+ img, transformer, net)
        tmp = {
            'code48':code,
            'label':id,
            'img':img,
            }
        db.insert(**tmp)
        count += 1
        if count%1000 == 0:
            db.commit()
    print 'build db ok, total is {}'.format(count)

cc = COCO(ann_file)

imgs = []
for id, value in cc.imgs:
    imgs.append((id, value['file_name']))

print 'imgs has {} imgs'.format(len(imgs))

db = database('coco')
build_db(db)
