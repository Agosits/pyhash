from . import *
from .utils import network
def build_db(img_list, db, transformer, net):
    db.create_table()
    print '***** build_db opt={} *****'.format(opt)
    id = db.maxid()
    for img in img_list:
        id += 1
        hashcode, fc7 = network(caffe_root + img, transformer, net)
        db.insert(code48=hashcode, img=img)
        # np.save(npys_path + '{}.npy'.format(id), fc7)
        if id % 100 == 0:
            print '***** id = {},tot = {} *****'.format(id, len(img_list))
    db.commit()

if __name__ == '__main__':
    net, transformer = net_init()
    print '***** step = {} *****'.format(step)
    # db
    db = database()
    if step == 0:
        build_db(img_list, db, transformer, net)
    else:
        query_img = '/examples/cvprw15-cifar10/imgs/bus2.jpg'
        coarse_time, fine_time, result = query(query_img, db, transformer, net, step)
        for img in result:
            print img
    db.close()
