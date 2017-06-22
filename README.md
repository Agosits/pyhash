# pyhash
### 需要简单了解
+ sql
+ sqlite
+ gunicorn
+ supervisor  
+ flask
+ redis

sql+sqlite主要是用来操作数据库，因为是小网站没有什么模型所以没用django，用了flask。<br>
redis用来存储特征，一个cifar就1.2G了。直接启动是rdb模式，redis自带的conf被我改成aof模式了，相应的文件都有。内存不够用aof，够就用rdb。<br>
gunicorn是服务器，因为当时nginx有着别人的东西，所以用这个代替了。<br>
supervisor并没有进行进程守护，被我用来做日志管理了。相关配置在`/hoem/wzq/supervisor`下
### 启动与运行
***
首先启动虚拟环境
`source /home/wzq/.bash_custom` 命令行最前面出现（wzq）说明虚拟环境启动成功
+ 路径
caffe-cvprw15/
    pyhash/
    dbfille
demo.db、hash.db 和 pyhash同级
+ 启动web
  + 启动redis 
`cd /home/wzq/redis-3.2.8/src/
  ./redis-server & `
redis启动需要一定的时间，默认rdb save模式。
redis-3.2.8/有一个redis.conf，配置了aof模式。
看到redis加载完db文件，可以接受6379端口的请求说明redis启动完毕。
  + 启动 supervisor, supervisor会去启动gunicorn<br>
/home/wzq 目录下有一个start_supervisor.sh，运行即可.<br>
还有一个 start_gunicorn.sh 不使用supervisor，缺点是关闭的时候需要kill，日志直接输出。<br>
pyhash/目录下有gc.conf。是gunicorn的配置文件
端口被设置为5001，启动后可以访问。

可能supervisor已经被启动了，但是web没有启动。
 ```
cd  /home/wzq/supervisor
supervisorctl -c supervisor.conf
```
进入supervisor控制台应该可以看到web stopped 这一信息。`start web`即可。
* 关闭
 ```
cd  /home/wzq/supervisor
supervisorctl -c supervisor.conf
```
进入supervisor的控制台，正常应该能看到名为web的app正在运行，和它的pid。`stop web`可以stop，`start web`可以重新激活。其他的操作请学习使用supervisor。
+ 日志
/home/wzq/log<br>
目前stdout.log是gunicorn的日志。日志大小设为了10M*10，即超过10M会自动分割新的文件，最多10个。配置在`/home/wzq/supervisor/app.ini`中。
如果没有使用supervisor，日志不会被捕获，直接输出。
***
运行pyhash下的某个文件，牵扯到其他文件的话，需要在pyhash一级运行
`python -m pyhash.xxxx`
***
### 模块介绍
+ settings.py
配置文件，opt用来指定数据集，主要用来控制数据库表名和相关的网络、模型文件。
step用来控制步骤，0是建库，1是粗分，2是粗分+细分。但是已经被废弃了，除了main应该没有地方在用了。

+ db.py
包含一个database类，对数据库的常用操作进行了封装。
  + init 接受一个参数，表名，用来指定表名。
  + insert `db.insert(key1=value1, key2=value2)`
  + query __哈希检索__，3个参数，哈希码，哈希码长，汉明距离阈值。其中码长默认为48，阈值默认是5.返回哈希检索的结果
  + create_table。创建表。接受一个参数，码长，默认为48。字段包括
 
id | code48 | img | label
----|------|----|---
id | 哈希码  | 图片路径 | 标签

+ web.py 网页后台的业务逻辑
+ utils.py  封装的函数 
  + timing 计时装饰器
  + network 图片过网络，返回哈希码和fc7层特征。如果网络换了，这个地方要重写。
  + fine_match 细分。redis
  + fine_match_back 老版本的细分。npy
  + web_query  web用到的查询。分为3各部分，粗分，不粗分的细分，基于粗分的细分。因为不粗分的细分太太太慢了，所以被我注释掉了。返回三个不同的结果和耗时。目前只用了粗分和基于粗分的细分。
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
建库的模版在coco.py里。
大致流程：
```
rd # from settings import rd , redis
db=database('dbname')
db.create_table()
for img in imgs:
  code, fc7 = network(img, *其他参数)
  db.insert(codeX=code, img=img, label=xxx) #保存信息到sqlite数据库
  key = {}_{} .format(table_name, id) # cifar_1, mnist_222, coco_12345 这种
  rd.set(key,fc7) #保存fc7到redis
db.commit()
db.close()
 ```
可能你需要对数据库进行一些自定义的操作,db.py里大多数都是这样的操作，可以参考
```
import sqlite3 as sq
db = sq.connect('xxxxx.db')
sql = 'your sql such as select * from table '
db.execute(sql)
db.commit()
db.close()
```
检索请参考utils.py里的web_query。
***
其实只有db和utils写的还行，其他的都很差。settings觉得写成dict式的配置不知道比函数和if语句好到哪里去了，建议新的项目使用db和utils，其他的推倒重写-_-。sorry！
