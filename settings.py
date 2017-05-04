import redis

opt = 'cifar' # demo or cifar or mnist
# 0 for build,others for query; 1 for coarse; 2 for fc7; 3 for both
step = 3

caffe_root = '/home/fious/gitroom/caffe-cvprw15'
caffe_path = '/home/fious/gitroom/caffe/'

mean_file = caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy'

def get_files():
    if opt == 'demo' or opt == 'cifar':
        model_weights = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48.caffemodel'
        model_def = caffe_root+'/examples/cvprw15-cifar10/KevinNet_CIFAR10_48_deploy.prototxt'
    elif opt == 'mnist':
        #model_def = caffe_path + 'examples/mnist/lenet_64.prototxt'
        model_def = caffe_path + 'examples/mnist/lenet_{}.prototxt'
        model_weights = caffe_path + 'examples/mnist/lenet_{}.caffemodel'
    return model_weights, model_def

def get_img_list():
    if opt == 'demo':
        img_list_file = caffe_root + '/img_list.txt'
    elif opt == 'cifar':
        img_list_file = caffe_root + '/examples/cvprw15-cifar10/dataset/train-file-list.txt'
    else:
        print 'There is no img list'
        return

    with open(img_list_file) as f:
        return [line.strip() for line in f.readlines()]

if opt =='cifar':
    npys_path = './pyhash/npys/'
    dbfile = 'hash.db'
    table_name = 'cifar'
elif opt == 'demo':
    npys_path = './pyhash/npys_demo/'
    dbfile = 'demo.db'
    table_name = 'demo'
elif opt == 'mnist':
    dbfile = 'hash.db'
    table_name = 'mnist'
    npys_path = None

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
rd = redis.Redis(connection_pool=pool)
