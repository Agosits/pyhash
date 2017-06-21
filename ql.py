import math
from random import randint
from . import *
from .k_accurate import img_list, img_labels
from .settings import table_name
from .utils import network


model_weights = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_{}.caffemodel'
model_def = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_deploy{}.prototxt'
qs = [12, 32, 48, 64]


def build_db(db, net, transformer):

    imgs = get_img_list()
    for i,img in enumerate(imgs):
        id = i+1
        #if id< 49002:
        #    continue
        code, _ = network(caffe_root + img, transformer, net)
        sql = 'UPDATE {} SET code{}="{}" WHERE id={};'.format(
            table_name, q, code, id)
        print id,sql
        db.db.execute(sql)
        if id % 100 == 0:
            print id
            db.commit()

def cal_acc(T=100):
    l = [randint(0, 10000) for i in range(0,T)]
    for i in l:
        img = imgs[i]
        code, _ = network(caffe_root + img, transformer, net)
        _, result = db.query(code, length=q, threshold=int(math.ceil(float(q)/10)))
        result = [item[3] for item in result]#[:1000]

        target_label = int(labels[i])
        hit = 0
        #ac = []
        for label in result:
            #print 'lable={},target_label={}'.format(label, target_label)
            if int(label) == target_label:
                hit += 1
        if len(result) == 0:
            print i,img
        else:
            print 'hit={},k={}'.format(hit,len(result))
            ac.append(float(hit)/len(result))

if __name__ == '__main__':
    db = database()
    d = {}
    for q in qs:
        #if q != 32:
        #    continue
        print '***** q =={}'.format(q)
        weights = model_weights.format(q)
        prototxt = model_def.format(q)

        net = caffe.Net(prototxt, weights, caffe.TEST)
        mu = np.load(mean_file)
        mu = mu.mean(1).mean(1)
        print 'mean-subtracted values:', zip('BGR', mu)

        # create transformer for the input called 'data'
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

        transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
        transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
        transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

        net.blobs['data'].reshape(1,        # batch size
                                  3,         # 3-channel (BGR) images
                                  227, 227)  # image size is 227x227

        # ---

        #build_db(db, net, transformer)
        #continue
        with open(img_list) as f:
            imgs = [line.strip() for line in f.readlines()]
        with open(img_labels) as f:
            labels = [int(line.strip()) for line in f.readlines()]
        ac = []
        cal_acc()

        d[q]=float(sum(ac))/len(ac)
    for k,v in d.items():
        print k,v
    db.close()
