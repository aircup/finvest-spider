# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
from scrapy.conf import settings


class FinvestPipeline(object):

    def __init__(self):
        """
        use for connecting to mongodb
        """
        # connect to db
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # ADD if NEED account and password
        # self.client.admin.authenticate(host=settings['MONGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        content = item['content']
        
        content = content.replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
        # delete html label in content
        rule = re.compile(r'<[^>]+>', re.S)
        content = rule.sub('', content)

        item['content'] = content
        self.coll.insert(dict(item))
        return item
