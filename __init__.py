# encoding:utf-8
import sys
import numpy as np

from .db import database
from .utils import query, fine_match
from .settings import *

sys.path.insert(0, caffe_path+'python')
import caffe

caffe.set_mode_cpu()
img_list = get_img_list()
weights, prototxt = get_files()

def net_init():
    # default net init, cifar net length=48
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
    return net, transformer
