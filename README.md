# pyhash
***
+ pip install flask redis lmdb
+ sqlite 可视化工具推荐 sqlitebrowser
***
+ 路径
caffe-cvprw15/
    pyhash/
    dbfille
demo.db、hash.db 和 pyhash同级
+ 启动web
  + 启动redis 
`cd ~/redis-3.2.8/src/
  ./redis-server & `
redis启动需要一定的时间，默认rdb save模式。
redis-3.2.8/有一个redis.conf，配置了aof模式。
看到redis加载完db文件，可以接受6379端口的请求说明redis启动完毕。
  + 启动 gunicorn
~目录下有一个start_web.sh，运行即可
pyhash/目录下有gc.conf。是gunicorn的配置文件
端口被设置为5001，启动后可以访问。
***
运行pyhash下的某个文件，牵扯到其他文件的话，需要在pyhash一级运行
`python -m pyhash.xxxx`
***
主要文件
+ settings.py 配置文件
+ web.py 后台业务逻辑
+ db.py 数据库部分操作的封装
+ utils.py 乱七八糟的函数

其他的文件是跑实验的代码
+ ql cifar不同长度哈希码
+ k_acc cifar topk
+ mnist mnist两个实验
+ coco  coco
+ main 最初的demo
***
settings 
+ opt 主要用来指定数据库表，不过现在数据库初始化的时候可以传入表名覆盖掉。
+ step  最初用来控制步骤的标志，除了main应该没有地方在用了

utils 里有一个fine_match 和 fine_match_back，back是以前的npy检索，现在的是redis。redis是最后加的需求，所以以前的都没有改，只有web用到了特征检索。
***
运行的大体流程一般是
+ init 初始化参数，读取settings
+ 初始化网络
+ 处理
***
在一个数据集上检索的流程一般是
+ model 和 prototxt
+ 建好数据库，db里面有一个create_table，最好自己写吧。
+ 写脚本 build db
+ 检索
***
其实只有db和utils写的还行，其他的都很差。settings觉得写成dict式的配置不知道比函数和if语句好到哪里去了，建议新的项目使用db和utils，其他的推倒重写-_-。sorry！
