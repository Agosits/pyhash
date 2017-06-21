import lmdb
from random import randint
from matplotlib import pyplot

from . import *

lmdb_file = caffe_path + 'examples/mnist/mnist_train_lmdb'
#qs = [8, 16,32,64,128]
qs = [48]
ks = [10, 200, 400, 600, 800, 1000]

def to_label(x):
    net.blobs['data'].data[...] = x
    net.forward()
    output = net.forward()['loss']
    data = net.blobs['fc8_pascal'].data
    print data
    max = 0
    x = 100
    for i, p in enumerate(data.tolist()[0]):
        if p>max:
            max = p
            x= i
    return x

def trans(value):
    datum = caffe.proto.caffe_pb2.Datum()#datum类型
    datum.ParseFromString(value)#转成datum
    flat_x = np.fromstring(datum.data, dtype=np.uint8)#转成numpy类型
    x = flat_x.reshape(datum.channels, datum.height, datum.width)#reshape大小
    y = datum.label#图片的label
    return x[0],y

def network(x):
    net.blobs['data'].data[...] = x
    net.forward()
    output = net.forward()['fc8_kevin_encode']
    l = output.tolist()
    code = [str(1) if i>0.5 else str(0) for i in l[0]]
    code = ''.join(code)
    return code

def build_db(db,length):
    count = 0
    s='code{}'.format(length)
    with lmdb.open(lmdb_file, readonly=True) as env:
        with env.begin() as txn:
            with txn.cursor() as curs:
                for key, value in curs:
                    x,y = trans(value)
                    code = network(x)
                    if q == 8:
                        d = {s:code,
                         'label':y,
                         'img':key
                         }
                        db.insert(**d)
                    else:
                        sql = 'UPDATE {} SET code{}="{}" WHERE id={};'.format(
                            db.name, q, code, count+1)
                        print key, sql
                        db.db.execute(sql)

                    count += 1
                    if count % 1000 == 0:
                        print count
                        db.commit()
                        #exit(0)
    print count
    db.commit()

def generate_random_img(T):
    l = [randint(0,60000) for i in range(0, T)]
    random_keys = []
    for i in range(0, T):
        s = str(l[i])
        for j in range(0, 8-len(s)):
            s = '0' + s
        random_keys.append(s)

    result = []
    with lmdb.open(lmdb_file, readonly=True) as env:
        with env.begin() as txn:
            with txn.cursor() as curs:
                for key in random_keys:
                    result.append(curs.get(key))
    return result

def cal_accu(T=100):
    tot = 0
    datums = generate_random_img(T)
    for datum in datums:
        x, y = trans(datum)
        code = network(x)
        _, result = db.query(code, length=q, threshold=q/10)
        result = [int(i[3]) for i in result]
        hit = 0
        for i in result:
            if i == int(y):
                hit += 1

        ac = float(hit)/len(result)
        print 'hit = {}, k ={}'.format(hit, len(result))
        print 'ac = {}'.format(ac)
        tot += ac
    print 'total ac:'
    print tot/T
    ans[q] = tot/T

def k_acc(T=10):
    datums = generate_random_img(T)
    ac = []
    d = 0
    for datum in datums:
        x, y = trans(datum)
        code = network(x)
        _, result = db.query(code, length=q, threshold=q/10)
        result = [int(i[3]) for i in result]

        if len(result)<ks[-1]:
            d += 1
            continue
        p = hit = 0
        for k in ks:
            while p<k:
                if result[p] == int(y):
                    hit += 1
                p += 1
            print 'hit={},k={}'.format(hit,k)
            ac.append(float(hit)/k)

    result = []
    for i in range(0, len(ks)):
        tot = 0
        for j in range(0, T-d):
            tot += ac[i+j*len(ks)]
        result.append(tot/(T-d))
    return result

if __name__ == '__main__':

    db = database()
    ans = {}
    k_ans = []
    #db.create_table(length=64)
    for q in qs:
        net = caffe.Net(prototxt.format(q), weights.format(q), caffe.TEST)
        #build_db(db, length=q)

        #cal_accu()
        k_ans.append(k_acc())

    #for key, value in ans.items():
    #    print key,value
    for ans in k_ans:
        print ans
