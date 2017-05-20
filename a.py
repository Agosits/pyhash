from settings import caffe_path
import sys
print sys.path
print '-----'
sys.path.insert(0, caffe_path+'python')
import caffe
print 'ok'
