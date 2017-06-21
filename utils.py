import os
import time
import caffe
import numpy as np

from .settings import opt, caffe_root, npys_path, rd

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

def str2npy(s):
    l = s.split(',')
    npy = np.array( [float(i) for i in l] )
    return npy

@timing('fine_match')
def fine_match_back(fc7, candidate, k, db):
    dist_dict = {}
    if candidate:
        for img in candidate:
            id = img[0]
            key = '{}_{}'.format(opt, id)
            value = rd.get(key)
            if value:
                c_fc7 = str2npy(value)
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

@timing('fine_match')
def fine_match(fc7, candidate, k, db):
    dist_dict = {}
    if candidate:
        for img in candidate:
            id = img[0]
            key = '{}_{}'.format(opt, id)
            value = rd.get(key)
            if value:
                c_fc7 = str2npy(value)
                dist = np.linalg.norm(fc7 - c_fc7)
                dist_dict[img] = dist

    else:
        maxid = db.maxid()
        for id in range(1,maxid+1):
            key = '{}_{}'.format(opt, id)
            value = rd.get(key)
            if value:
                c_fc7 = str2npy(value)
                dist = np.linalg.norm(fc7 - c_fc7)
                dist_dict[id] = dist

    sorted_tuples = sorted(dist_dict.items(), key=lambda item:item[1])[:k]

    #exit(0)
    if candidate:
        imgs = [tup[0][2] for tup in sorted_tuples]
    else:
        ids = [tup[0] for tup in sorted_tuples]
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
        result = [item[0] for item in result]

    return coarse_time, fine_time, result

def web_query(query_img, db, transformer, net):
    hashcode, fc7 = network(caffe_root + query_img, transformer, net)
    # coarse match
    coarse_time, coarse_result = db.query(hashcode)

    # fine match
    k = 50
    fine_time, fine_result = None, None#fine_match(fc7, None, k, db)

    #both
    both_time, both_result = fine_match(fc7, coarse_result, k, db)
    both_time += coarse_time

    coarse_result = [item[2] for item in coarse_result][:k]
    print coarse_time,  both_time, coarse_result, both_result
    #exit(0)
    return coarse_time, fine_time, both_time, coarse_result, fine_result, both_result
