from . import *
from .utils import network
from .settings import table_name
from random import randint

label_file = caffe_root + '/examples/cvprw15-cifar10/dataset/train-label.txt'
ks = [10, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
img_list = caffe_root + '/examples/cvprw15-cifar10/dataset/test-file-list.txt'
img_labels = caffe_root + '/examples/cvprw15-cifar10/dataset/test-label.txt'
net, transformer = net_init()

def add_label_to_db(db):
    with open(label_file) as f:
        labels = [line.strip() for line in f.readlines()]
    for i,label in enumerate(labels):
        id = i + 1
        sql = 'UPDATE {} set label={} WHERE id={};'.format(
            table_name, label, id
        )
        print sql
        #exit(0)
        db.db.execute(sql)

    db.commit()
    db.close()

def cal_accu(imgs, labels, T=100):
    l = [randint(0, 10000) for i in range(0,T)]
    for i in l:
        img = imgs[i]
        code, _ = network(caffe_root + img, transformer, net)
        _, result = db.query(code)
        result = [item[3] for item in result]

        if len(result)<ks[-1]:
            print 'sorry, result is < ks,len:{}'.format(len(result))
            continue

        target_label = int(labels[i])
        p = 0
        hit = 0
        ac = []
        for k in ks:
            while p<k:
                if int(result[p]) == target_label:
                    hit += 1
                p += 1
            #print 'hit={},k={}'.format(hit,k)
            if hit == 0:
                print target_label, result[p], imgs[i]
            ac.append(float(hit)/k)
        ans.append(ac)


if __name__ == '__main__':
    print 'kacc start'
    db = database()
    #add_label_to_db(db)
    with open(img_list) as f:
        imgs = [line.strip() for line in f.readlines()]
    with open(img_labels) as f:
        labels = [int(line.strip()) for line in f.readlines()]
    ans = []
    cal_accu(imgs, labels)
    for i,k in enumerate(ks):
        tot = 0
        for img_result in ans:
            tot += img_result[i]
        print k,tot/len(ans)
