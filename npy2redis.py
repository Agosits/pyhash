import os
import redis
import numpy as np

from .settings import npys_path, opt


#pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(host='127.0.0.1', port=6379)

# key= opt_id

npys = os.listdir(npys_path)
count = 0
print opt
for npy in npys:
    count += 1
    c_fc7 = np.load(npys_path + npy)
    l = c_fc7.tolist()
    s = ','.join([str(i) for i in l])
    id = int(npy[ :npy.index('.')])
    key = '{}_{}'.format(opt,id)
    r.set(key, s)

    if count%1000 == 0:
        print count
