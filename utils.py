import caffe
import numpy as np

from .settings import opt, caffe_root


def hamming_distance(s, t):
    x = 0
    for i in range(0,len(s)):
        if s[i] != t[i]:
            x += 1
    return x

def network(img, transformer, net):
    image = caffe.io.load_image(caffe_root + img)
    transformed_image = transformer.preprocess('data', image)

    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image

    net.forward()
    data = net.blobs['fc7'].data
    print data
    print type(data)
    print data.shape
    exit(0)
    output = net.forward()['fc8_kevin_encode']
    l = output.tolist()
    code = [str(1) if i>0.5 else str(0) for i in l[0]]
    code = ''.join(code)
    fc7 = net.forward()['fc7']
    return code, fc7
