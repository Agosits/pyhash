import sqlite3 as sq
import logging
import numpy as np

from .utils import hamming_distance, network,timing
from .settings import opt, npys_path, caffe_root, dbfile

logger = logging.getLogger('db')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class database(object):
    def __init__(self, code_length):
        self.db = sq.connect(dbfile)
        self.length = code_length

    def create_table(self, table_name=None):
        table_name = table_name or 'table_{}'.format(self.length)
        try:
            create_table = 'CREATE TABLE {} (\
                    id integer primary key not null,\
                    code varchar({}),\
                    img  varchar(100)\
                )'.format(table_name, self.length)
            self.db.execute(create_table)
            self.db.commit()
            print 'create_table {} success.'.format(table_name)
        except Exception as e:
            logger.error('create table {} failed'.format(table_name))
            logger.error(repr(e))

    def insert(self, code, img_path):
        try:
            sql = 'INSERT INTO table_{} (code,img) VALUES ({},{});'.format(
                self.length, code, img_path
            )
            # print sql
            self.db.execute(sql)
        except Exception as e:
            logger.error('insert failed')
            logger.error(repr(e))
            exit(0)

    def maxid(self, recall=False):
        try:
            sql = 'SELECT max(id) FROM table_{}'.format(self.length)
            tmp = self.db.execute(sql)
            for i in tmp:
                result = i[0]
                break
        except Exception as e:
            if not recall:
                logger.warning(repr(e))
                print 'thereis no table in the db at begining...'
                self.create_table()
                return self.maxid(recall=True)
            else:
                logger.error('get max id failed')
                logger.error(repr(e))
        else:
            if result:
                return result
        return 0

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    @timing('coarse match')
    def query(self, code ,threshold=5):
        cur = self.db.cursor()
        sql = 'SELECT id,code,img FROM table_{}'.format(self.length)
        tmp = cur.execute(sql)
        result = []
        for row in tmp:
            if hamming_distance(code, row[1]) <= threshold:
                result.append(row)
        cur.close()
        return result

    def fetch_img_path(self, ids):
        cur = self.db.cursor()
        sql = 'SELECT id,img FROM table_{} WHERE id IN {}'.format(self.length, tuple(ids))
        print sql
        tmp = cur.execute(sql)
        result = []
        for row in tmp:
            result.append(row[1])
        cur.close()
        return result

def build_db(img_list, db, transformer, net):
    print '***** build_db opt={} *****'.format(opt)
    id = db.maxid()
    for img in img_list:
        id += 1
        hashcode, fc7 = network(caffe_root + img, transformer, net)
        db.insert('"'+hashcode+'"', '"'+img+'"')
        np.save(npys_path + '{}.npy'.format(id), fc7)
        if id % 100 == 0:
            print '***** id = {},tot = {} *****'.format(id, len(img_list))
    db.commit()
