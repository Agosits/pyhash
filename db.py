import sqlite3 as sq
import logging
import numpy as np

from .utils import hamming_distance, network,timing
from .settings import opt, npys_path, caffe_root, dbfile, table_name

logger = logging.getLogger('db')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class database(object):
    def __init__(self, name=None):
        name = name or table_name
        self.db = sq.connect(dbfile)
        self.name = name

    def create_table(self, length=48):
        try:
            create_table = 'CREATE TABLE {} (\
                    id integer primary key not null,\
                    code{} varchar(100),\
                    img  varchar(100),\
                    label varchar(100)\
                )'.format(self.name, length)
            self.db.execute(create_table)
            self.db.commit()
            print 'create_table {} success.'.format(self.name)
        except Exception as e:
            logger.error('create table {} failed'.format(self.name))
            logger.error(repr(e))

    def insert(self, *args, **kwargs):
        keys = kwargs.keys()
        values = []
        for key in keys:
            values.append(kwargs[key])
        try:
            sql = 'INSERT INTO {} {} VALUES {};'.format(
                self.name, tuple(keys), tuple(values)
            )
            print sql
            self.db.execute(sql)
        except Exception as e:
            logger.error('insert failed')
            logger.error(repr(e))
            exit(0)

    def maxid(self, recall=False):
        try:
            sql = 'SELECT max(id) FROM {}'.format(self.name)
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
    def query(self, code ,length=48, threshold=5):
        cur = self.db.cursor()
        sql = 'SELECT id,code{},img,label FROM {}'.format(length, self.name)
        tmp = cur.execute(sql)
        result = []
        for row in tmp:
            if hamming_distance(code, row[1]) <= threshold:
                result.append(row)
        cur.close()
        return result

    def fetch_img_path(self, ids):
        cur = self.db.cursor()
        sql = 'SELECT img,label FROM {} WHERE id IN {}'.format(self.name, tuple(ids))
        print sql
        tmp = cur.execute(sql)
        result = []
        for row in tmp:
            result.append(row[0])
        cur.close()
        return result
