# -*- coding: utf-8 -*-
import os
import sys
import psycopg2
from elasticsearch import Elasticsearch, helpers
from pymongo import MongoClient, errors, ASCENDING, DESCENDING
sys.path.append(os.path.abspath('.'))
from utils.data_utils import EnvReader  # noqa: E402

env = EnvReader()


class Postgresql:
    def __init__(self, database="wallet", platform="plt"):
        self.database = database

        if platform == "plt":
            self.host = env.POSTGRES_PLT_HOST
            self.port = env.POSTGRES_PLT_PORT
            self.user = env.POSTGRES_PLT_ACCOUNT
            self.password = env.POSTGRES_PLT_PASSWORD
        elif platform == "cs":
            self.host = env.POSTGRES_CS_HOST
            self.port = env.POSTGRES_CS_PORT
            self.user = env.POSTGRES_CS_ACCOUNT
            self.password = env.POSTGRES_CS_PASSWORD
        else:
            raise "platform Error"

        self.db = psycopg2.connect(database=self.database,
                                   user=self.user,
                                   password=self.password,
                                   host=self.host,
                                   port=self.port)

    def select_sql(self, sql):
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            raise Exception('Postgresql select_sql issue: %s' % str(e))
        finally:
            self.cursor.close()

    def run_sql(self, sql):
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("SQL Success")
        except Exception as e:
            self.db.rollback()
            raise Exception('Postgresql select_sql issue: %s' % str(e))

        finally:
            self.db.close()


class ElasticsearchTool:
    def __init__(self):
        self.host = env.ELASTICSEARCH_HOST
        self.port = env.ELASTICSEARCH_PORT
        self.user = env.ELASTICSEARCH_USER
        self.password = env.ELASTICSEARCH_PASSWORD

        self.es = Elasticsearch(hosts=self.host,
                                http_auth=(self.user, self.password),
                                port=self.port)

    def get_index(self):
        target = self.es.indices.get_alias().keys()
        return target

    def query(self, index, query_json, scroll='5m', size=100):
        target = self.es.search(index=index, query=query_json,
                                scroll=scroll, size=size)
        return target

    def add_data(self, index, doc_type, json_data):
        self.es.index(index=index, doc_type=doc_type, document=json_data)

    '''
    批量新增需在json裡就定義好_index跟doc_type
    用list來存放dict物件
    參考來源https://juejin.cn/post/7020586906744258573
    '''
    def add_bulk_data(self, json_body):
        helpers.bulk(self.es, body=json_body)


class Mongo:
    def __init__(self, platform):
        if platform == "plt":
            self.host = env.MONGO_PLT_HOST
            self.account = env.MONGO_PLT_ACCOUNT
            self.password = env.MONGO_PLT_PASSWORD
        elif platform == "cs":
            self.host = env.MONGO_CS_HOST
            self.account = env.MONGO_CS_ACCOUNT
            self.password = env.MONGO_CS_PASSWORD
        else:
            raise "platform error"

        conn_str = f'mongodb+srv://{self.account}:{self.password}@{self.host}'
        self.mongodb = MongoClient(conn_str, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
        # 檢查連線是否成功
        try:
            self.mongodb.server_info()
        except errors.ServerSelectionTimeoutError as e:
            raise Exception('MongoDB connection timeout: %s' % str(e))
        except Exception as e:
            raise Exception('MongoDB connection failed: %s' % str(e))

    def _check_db(self):
        if self.db is None:
            raise Exception('No database selected')

    def _check_collection(self):
        if self.collection is None:
            raise Exception('No collection selected')

    def _check_db_and_collection(self):
        self._check_db()
        self._check_collection()

    @staticmethod
    def _check_query(query):
        if not query:
            raise Exception('Query syntax should not be emtpy dict or list')

    @staticmethod
    def _check_query_type(query, query_type):
        if type(query) is not query_type:
            raise TypeError(f'Query syntax type error, \"{query}\" type must be {query_type}')
        if not query:
            raise Exception('Query syntax should not be emtpy dict or list')

    def specify_db(self, database):
        if database:
            db_list = self.mongodb.list_database_names()
            if database in db_list:
                self.db = self.mongodb[database]
                return self.db
            else:
                raise Exception('No db [%s] in specified MongoDB.' % database)
        else:
            raise Exception('Mongo connection must have specified param [database].')

    def specify_collection(self, collection):
        self._check_db()
        if collection:
            collection_list = self.db.list_collection_names()
            if collection in collection_list:
                self.collection = self.db[collection]
                return self.collection
            else:
                raise Exception(f'No collection {collection} in specified database {self.db}.')
        else:
            raise Exception('Mongo connection must have specified param [collection].')

    def find(self, query=None, projection=None, sort_key=None, sort_direction='DESC', limit=1):
        self._check_db_and_collection()
        try:
            query = query if query is not None else {}
            # 依排序條件執行查詢
            if sort_key:
                if sort_direction == 'ASC':
                    result = self.collection.find(filter=query, projection=projection).sort(sort_key, ASCENDING).limit(limit)
                elif sort_direction == 'DESC':
                    result = self.collection.find(filter=query, projection=projection).sort(sort_key, DESCENDING).limit(limit)
                else:
                    raise ValueError('param [key_direction] mush be "ASC" or "DESC".')
            else:
                result = self.collection.find(filter=query, projection=projection).limit(limit)

            result_list = []
            for x in result:
                result_list.append(x)
            return result_list
        except Exception as e:
            raise Exception('MongoDB query syntax issue: %s' % str(e))

    def insert_one(self, query):
        self._check_db_and_collection()
        # 檢查query資料型態是dict、並禁止使用empty dict
        self._check_query_type(query, dict)

        try:
            self.collection.insert_one(query)
        except Exception as e:
            raise Exception('MongoDB insert_one issue: %s' % str(e))

    def insert_many(self, query):
        self._check_db_and_collection()
        # 檢查query資料型態是list、並禁止使用empty list
        self._check_query_type(query, list)

        try:
            self.collection.insert_many(query)
        except Exception as e:
            raise Exception('MongoDB insert_many issue: %s' % str(e))

    def update_one(self, filter_query, update_query):
        self._check_db_and_collection()
        # 檢查query資料型態是dict、並禁止使用empty dict
        self._check_query_type(filter_query, dict)
        self._check_query_type(update_query, dict)

        try:
            self.collection.update_one(filter_query, update_query)
        except Exception as e:
            raise Exception('MongoDB update_one issue: %s' % str(e))

    def delete(self, query):
        self._check_db_and_collection()
        # 檢查query資料型態是dict、並禁止使用空{}
        self._check_query_type(query, dict)

        try:
            self.collection.delete_many(query)
        except Exception as e:
            raise Exception('MongoDB delete issue: %s' % str(e))


if __name__ == '__main__':
    # PostgreSQL sample
    pg = Postgresql(database='plt_account')
    sql = "select * from plt_account.plt_account.ldpro_role where id = 3;"
    print(pg.select_sql(sql=sql))

    # ES sample
    # import json

    # def printJson(func):
    #     print(json.dumps(func, sort_keys=True, indent=4, separators=(',', ':')))
    # test = ElasticsearchTool()
    # abc = {"match": {"user_id": "66"}}
    # t = test.query(index='ldpro_wallet_log', query_json=abc, size=1)
    # printJson(t)

    # MongoDB sample
    # mongo = Mongo(platform='plt')
    # mongo.specify_db('plt_game')
    # mongo.specify_collection('ldpro_mer_user')

    # test_mongo_update_user_status
    # filter_query = {"username": "proxyAccount62226"}
    # update_query = {"$set": {"lock_status": {"LOGIN": True, "RECHARGE": True, "WITHDRAW": True, "TRANSFER": True}}}
    # mongo.update_one(filter_query, update_query)

    # demo insert_one and insert_many method
    # query_insert = {"name": "insert_one_test", "channel_code": "1", "game_code": "1", "user_id": 1}
    # query_insert_many = [
    #     {"name": "insert_two_test", "channel_code": "2", "game_code": "2", "user_id": 1},
    #     {"name": "insert_three_test", "channel_code": "3", "game_code": "3", "user_id": 1}
    # ]
    # mongo.insert_one(query_insert)
    # mongo.insert_many(query_insert_many)
    # result = mongo.find(limit=10)
    # for detail in result:
    #     print(detail)
    # print('--------------------')

    # # demo delete method
    # mongo.delete(query={"user_id": 1})
    # result = mongo.find(limit=10)
    # for detail in result:
    #     print(detail)
