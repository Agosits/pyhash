import os
from flask import Flask, request,render_template
from . import *

tmp_img_file = r'./pyhash/tmp.jpg'
app = Flask(__name__,static_url_path='',static_folder=caffe_root)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/query", methods=['POST', 'GET'])
def img_query():
    #return 'Hello'
    img_file = request.files['img']
    img_path = tmp_img_file
    if os.path.exists(img_path):
        os.remove(img_path)
    img_file.save(img_path)
    step = int(request.values.get('step', 1))
    #----------------
    db = database(48)

    coarse_time, fine_time, result = \
        query(img_path.strip('.'), db, transformer, net, step)
    #result = [{'file'}]
    return render_template('result.html',result=result,
                                         coarse_time=coarse_time,
                                         fine_time = fine_time)
