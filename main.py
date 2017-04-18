# encoding:utf-8
import sys
import numpy as np
from .inputdata import get_img_list
from .setup import caffe_setup
from .db import database,build_db

caffe_root = '/home/fious/gitroom/caffe-cvprw15'
caffe_path = '/home/fious/gitroom/caffe/'
sys.path.insert(0, caffe_path+'python')

# caffe_setup
import caffe
caffe.set_mode_cpu()
model_weights = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48.caffemodel'
model_def = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48_deploy.prototxt'
mean_file = caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy'
net, transformer = caffe_setup(caffe_root,
    weights=model_weights, prototxt=model_def, mean_file=mean_file)
# --------------------------------------------------------

opt = 'demo' # demo or cifar
step = 0 # 0 for coarse hash; 1 for fc7 ; 2 for both

# input img_list
img_list = get_img_list(caffe_root, opt)
print len(img_list)

# db
db = database(48)
build_db(img_list, db, opt)
