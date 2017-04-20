from . import *

if __name__ == '__main__':
    print '***** step = {} *****'.format(step)
    # db
    db = database(48)
    if step == 0:
        build_db(img_list, db, transformer, net)
    else:
        query_img = '/examples/cvprw15-cifar10/imgs/bus2.jpg'
        coarse_time, fine_time, result = query(query_img, db, transformer, net)
        for img in result:
            print img
    db.close()
