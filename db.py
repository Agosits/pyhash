import sqlite3 as sq
import logging

from .utils import hamming_distance, network
from .settings import opt

logger = logging.getLogger('db')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class database(object):
    def __init__(self, code_length):
        self.db = sq.connect('hash.db')
        self.length = code_length

    def create_table(self, table_name=None):
        table_name = table_name or 'table_{}'.format(self.length)
        try:
            create_table = 'CREATE TABLE {} ( \
                    code varchar({}), img  varchar(100) \
                )'.format(table_name, self.length)
            self.db.execute(create_table)
            self.db.commit()
        except Exception as e:
            logger.error('create table {} failed'.format(table_name))
            logger.error(repr(e))

    def insert(self, code, img_path, recall=False):
        try:
            sql = 'INSERT INTO table_{} (code,img) VALUES ({},{});'.format(
                self.length, code, img_path
            )
            #print sql
            self.db.execute(sql)
        except Exception as e:
            if not recall:
                logger.warning(repr(e))
                self.create_table()
                self.insert(code, img_path, recall=True)
            else:
                logger.error('insert failed')
                logger.error(repr(e))
                exit(0)
    def query(self, code ,threshold=5):
        cur = self.db.cursor()
        sql = 'SELECT code,img FROM table_{}'.format(self.length)
        tmp = cur.execute(sql)
        result = []
        for row in tmp:
            if hamming_distance(code, row[0]) <= threshold:
                result.append(row)
        cur.close()
        return result

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

def build_db(img_list, db, transformer, net):
    print '***** build_db opt={} *****'.format(opt)
    for img in img_list:
        hashcode, fc7 = network(img, transformer, net)
        #db.insert('"'+hashcode+'"', '"'+img+'"')

        print fc7.shape
        exit(0)
    #save
