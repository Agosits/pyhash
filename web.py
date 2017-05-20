import os
from flask import Flask, request,render_template
from . import *
from .utils import web_query, network

tmp_img_file = r'./pyhash/tmp.jpg'
app = Flask(__name__,static_url_path='',static_folder=caffe_root)
net, transformer = net_init()

@app.route("/")
def index():
    return render_template('test.html')

@app.route("/query", methods=['POST', 'GET'])
def img_query():
    #return 'Hello'
    img_file = request.files['img']
    img_path = tmp_img_file
    if os.path.exists(img_path):
        os.remove(img_path)
    img_file.save(img_path)
    #----------------
    db = database()

    coarse_time, fine_time, both_time, coarse_result, fine_result, both_result = \
        web_query(img_path.strip('.'), db, transformer, net)
    #result = [{'file'}]
    return render_template('result.html',origin_file=img_path,
                            coarse_time=coarse_time, coarse_result=coarse_result,
                            fine_time = fine_time, fine_result=fine_result,
                            both_time = both_time, both_result=both_result,
                                         )

@app.route("/coco")
def coco():
    from .coco import cc, pre_path
    key = cc.imgs.keys()[0]
    img = cc.imgs[key]['file_name']
    input_url = cc.imgs[key]['coco_url']
    code, _ = network(pre_path + 'train2014/' + img, transformer, net)
    coarse_time, coarse_result = db.query(code)
    ids = [int(item[3]) for item in coarse_result]
    urls = [cc.imgs[id]['coco_url'] for id in ids]
    return render_template('coco.html', input=input_url, time=coarse_time, urls=urls)


if __name__ == '__main__':
    app.run()
