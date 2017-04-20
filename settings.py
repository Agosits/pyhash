opt = 'demo' # opt or cifar for now
# 0 for build,others for query; 1 for coarse; 2 for fc7; 3 for both
step = 1

caffe_root = '/home/fious/gitroom/caffe-cvprw15'
caffe_path = '/home/fious/gitroom/caffe/'

mean_file = caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy'

def get_files():
    if opt == 'demo' or opt == 'cifar':
        model_weights = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48.caffemodel'
        model_def = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48_deploy.prototxt'
    else:
        print 'sorry, we dont have this option'
        exit(0)
    return model_weights, model_def

def get_img_list():
    if opt == 'demo':
        img_list_file = caffe_root + '/img_list.txt'
    elif opt == 'cifar':
        img_list_file = caffe_root + '/examples/cvprw15-cifar10/dataset/train-file-list.txt'

    with open(img_list_file) as f:
        return [line.strip() for line in f.readlines()]

if opt =='cifar':
    npys_path = './pyhash/npys/'
    dbfile = 'hash.db'
elif opt == 'demo':
    npys_path = './pyhash/npys_demo/'
    dbfile = 'demo.db'
