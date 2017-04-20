import os
import time
import caffe
import numpy as np

from .settings import opt, caffe_root, npys_path

def timing(func_name):
    def deco_wrapper(func):
        def deco(*args, **kwargs):
            print '***** {} timing start *****'.format(func_name)
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print '***** {} :time consuming: {}s'.format(func_name, end-start)
            return end-start, result
        return deco
    return deco_wrapper

def hamming_distance(s, t):
    x = 0
    for i in range(0,len(s)):
        if s[i] != t[i]:
            x += 1
    return x

def network(img, transformer, net):
    image = caffe.io.load_image(img)
    transformed_image = transformer.preprocess('data', image)

    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image

    net.forward()
    data = net.blobs['fc7'].data
    fc7 = data[0]
    output = net.forward()['fc8_kevin_encode']
    l = output.tolist()
    code = [str(1) if i>0.5 else str(0) for i in l[0]]
    code = ''.join(code)
    return code, fc7

@timing('fine_match')
def fine_match(fc7, candidate, k, db):
    dist_dict = {}
    if candidate:
        for img in candidate:
            id = img[0]
            c_fc7 = np.load(npys_path + '{}.npy'.format(id))
            dist = np.linalg.norm(fc7 - c_fc7)
            dist_dict[img] = dist

    else:
        npys = os.listdir(npys_path)
        for npy in npys:
            c_fc7 = np.load(npys_path + npy)
            dist = np.linalg.norm(fc7 - c_fc7)
            dist_dict[npy] = dist

    sorted_tuples = sorted(dist_dict.items(), key=lambda item:item[1])[:k]
    print sorted_tuples
    #exit(0)
    if candidate:
        imgs = [tup[0][2] for tup in sorted_tuples]
    else:
        npys = [tup[0] for tup in sorted_tuples]
        ids = [int(npy[ :npy.index('.')]) for npy in npys]
        imgs = db.fetch_img_path(ids)
    return imgs

def query(query_img, db, transformer, net, step):
    hashcode, fc7 = network(caffe_root + query_img, transformer, net)

    result = []
    coarse_time = fine_time = None
    # coarse match
    if step == 1 or step == 3:
        coarse_time, result = db.query(hashcode)
        if step ==1:
            result = [item[2] for item in result]
    # fine_match
    if step == 2 or step == 3:
        k = 1000
        if result:
            k = min(k, len(result))
        fine_time, result = fine_match(fc7, result, k, db)

    return coarse_time, fine_time, result
