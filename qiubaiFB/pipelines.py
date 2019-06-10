# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import json
import pymysql


class QiubaifbPipeline(object):
    conn = None
    cursor = None
    redis_cli=None
    def open_spider(self, spider):
        print('开始爬虫')
        # 连接数据库
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123', db='spider')

    def process_item(self, item, spider):
        #
        # 指定redis数据库信息
        self.redis_cli = redis.StrictRedis(host='192.168.199.108', port=6379, db=0)
        # data = json.loads(self.redis_cli.get('redisQB:items'))

        source, data = self.redis_cli.blpop(["redisQB:items"])
        data_json=json.loads(data)
        # 1.连接数据库
        # 2.执行sql语句
        # sql = 'insert into qiubai VALUES("%s","%s")' % (item['author'], item['content'])
        sql = 'insert into qiubai VALUES("%s","%s")' % ('img', data_json['img_url'])
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

            self.conn.rollback()
        # 3.提交事务

        return item

    def close_spider(self, spider):
        print('爬虫结束')
        self.cursor.close()
        self.conn.close()
