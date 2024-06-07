import os
import json5
import copy
import configparser
import inspect

config = configparser.ConfigParser()
config.read('config/config.ini')


class TestDataReader:
    __test__ = False

    def __init__(self):

        if os.getenv('MODE') is None:
            self.file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'resources/dev/platform')
            self.cs_file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'resources/dev/client_side')
            self.case = None
        else:
            self.file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'resources/regression/platform')
            self.cs_file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'resources/regression/client_side')
            self.case = None

    def read_json5(self, json_file, file_side='plt') -> None:
        test_data = []
        key_data = []
        if file_side == 'cs':
            data_path = os.path.join(self.cs_file_path, json_file)
        else:
            data_path = os.path.join(self.file_path, json_file)

        with open(data_path, mode='r', encoding='utf8') as f:
            json_data = json5.load(f)
            for line in json_data:
                value1 = []
                key1 = []
                for k1, v1 in line.items():
                    if k1 != "test_item":
                        value1.append(v1)
                        key1.append(k1)
                    else:
                        for l1 in v1:
                            value2 = []
                            key2 = []
                            for k2, v2 in l1.items():
                                value2.append(v2)
                                key2.append(k2)
                            test_data.append(tuple(value1 + value2))
                            key_data.append(tuple(key1 + key2))  # 之後可能會用到
            test_case = []
            for i in range(len(key_data)):
                test_case.append(dict(zip(key_data[i], test_data[i])))
            self.case = test_case

    def get_case(self, target):
        if self.case is not None:
            testdata = []
            for i in self.case:
                if target == i["test_case"]:
                    testdata.append(i)
            return testdata
        else:
            raise ValueError("尚未載入Json檔案")

    @staticmethod
    def get_test_case(data, target):
        testdata = []
        for i in data:
            if target == i["test_case"]:
                testdata.append(i)
        return testdata

    @staticmethod
    def replace_json(json, target):
        json_copy = copy.deepcopy(json)  # 避免淺層複製導致case讀取有誤
        for key in list(target.keys()):

            value = target.get(key, "不存在")
            try:
                json_copy[key] = value
            except Exception:
                for item in json_copy:
                    item[key] = value
        return json_copy


class EnvReader:
    def __init__(self) -> None:
        self.env = os.getenv('MODE')
        self.__load_host()
        self.__load_postgres()
        self.__load_elasticsearch()
        self.__load_redis()
        self.__load_cs_test_account()
        self.__load_API_headers()
        self.__load_mongo()

    def __load_host(self):
        if os.getenv('MODE') is None:
            self.PLATFORM_HOST = config['host']['platform_host']
            self.WEB_HOST = config["host"]['web_host']
            self.XXL_HOST = config["host"]['xxl_host']
            self.CONTROL_HOST = config["host"]['control_host']
        else:
            self.PLATFORM_HOST = os.getenv('PLATFORM_HOST')
            self.WEB_HOST = os.getenv('WEB_HOST')
            self.XXL_HOST = os.getenv('XXL_HOST')
            self.CONTROL_HOST = os.getenv('CONTROL_HOST')

    def __load_postgres(self):
        if os.getenv('MODE') is None:
            self.POSTGRES_PLT_HOST = config['postgres_connection']['postgres_plt_host']
            self.POSTGRES_CS_HOST = config['postgres_connection']['postgres_cs_host']
            self.POSTGRES_PLT_PORT = config['postgres_connection']['postgres_plt_port']
            self.POSTGRES_CS_PORT = config['postgres_connection']['postgres_cs_port']
            self.POSTGRES_PLT_ACCOUNT = config['postgres_connection']['postgres_plt_account']
            self.POSTGRES_CS_ACCOUNT = config['postgres_connection']['postgres_cs_account']
            self.POSTGRES_PLT_PASSWORD = config['postgres_connection']['postgres_plt_password']
            self.POSTGRES_CS_PASSWORD = config['postgres_connection']['postgres_cs_password']
        else:
            self.POSTGRES_PLT_HOST = os.getenv('POSTGRES_PLT_HOST')
            self.POSTGRES_CS_HOST = os.getenv('POSTGRES_CS_HOST')
            self.POSTGRES_PLT_PORT = os.getenv('POSTGRES_PLT_PORT')
            self.POSTGRES_CS_PORT = os.getenv('POSTGRES_CS_PORT')
            self.POSTGRES_PLT_ACCOUNT = os.getenv('POSTGRES_PLT_ACCOUNT')
            self.POSTGRES_CS_ACCOUNT = os.getenv('POSTGRES_CS_ACCOUNT')
            self.POSTGRES_PLT_PASSWORD = os.getenv('POSTGRES_PLT_PASSWORD')
            self.POSTGRES_CS_PASSWORD = os.getenv('POSTGRES_CS_PASSWORD')

    def __load_elasticsearch(self):
        if os.getenv('MODE') is None:
            self.ELASTICSEARCH_HOST = config['elasticsearch_connection'][
                'elasticsearch_host']
            self.ELASTICSEARCH_PORT = config['elasticsearch_connection'][
                'elasticsearch_port']
            self.ELASTICSEARCH_USER = config['elasticsearch_connection'][
                'elasticsearch_user']
            self.ELASTICSEARCH_PASSWORD = config['elasticsearch_connection'][
                'elasticsearch_password']
        else:
            self.ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
            self.ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT')
            self.ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER')
            self.ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')

    def __load_redis(self):
        if os.getenv('MODE') is None:
            self.REDIS_PLT_HOST = config['redis_connection']['redis_plt_host']
            self.REDIS_CS_HOST = config['redis_connection']['redis_cs_host']
            self.REDIS_PLT_PORT = config['redis_connection']['redis_plt_port']
            self.REDIS_CS_PORT = config['redis_connection']['redis_cs_port']
            self.REDIS_PLT_PASSWORD = config['redis_connection'][
                'redis_plt_password']
            self.REDIS_CS_PASSWORD = config['redis_connection'][
                'redis_cs_password']
            self.REDIS_PLT_SENTINEL_LIST = eval(
                config['redis_connection']['redis_plt_sentinel_list'])
            self.REDIS_CS_SENTINEL_LIST = eval(
                config['redis_connection']['redis_cs_sentinel_list'])
            self.REDIS_SENTINEL_PLT_PASSWORD = config['redis_connection'][
                'redis_plt_sentinel_password']
            self.REDIS_SENTINEL_CS_PASSWORD = config['redis_connection'][
                'redis_cs_sentinel_password']
        else:
            self.REDIS_PLT_HOST = os.getenv('REDIS_PLT_HOST')
            self.REDIS_CS_HOST = os.getenv('REDIS_CS_HOST')
            self.REDIS_PLT_PORT = os.getenv('REDIS_PLT_PORT')
            self.REDIS_CS_PORT = os.getenv('REDIS_CS_PORT')
            self.REDIS_PLT_PASSWORD = os.getenv('REDIS_PLT_PASSWORD')
            self.REDIS_CS_PASSWORD = os.getenv('REDIS_CS_PASSWORD')
            self.REDIS_PLT_SENTINEL_LIST = os.getenv('REDIS_PLT_SENTINEL_LIST')
            self.REDIS_CS_SENTINEL_LIST = os.getenv('REDIS_CS_SENTINEL_LIST')
            self.REDIS_SENTINEL_PLT_PASSWORD = os.getenv(
                'REDIS_SENTINEL_PLT_PASSWORD')
            self.REDIS_SENTINEL_CS_PASSWORD = os.getenv(
                'REDIS_SENTINEL_CS_PASSWORD')

    def __load_cs_test_account(self):
        # if os.getenv('MODE') is None:
        self.CS_TEST_ACCOUNT = config['cs_account']['account']
        self.CS_TEST_PASSWORD = config['cs_account']['password']
        # else:
        #     self.CS_TEST_ACCOUNT = os.getenv('CS_TEST_ACCOUNT')
        #     self.CS_TEST_PASSWORD = os.getenv('CS_TEST_PASSWORD')

    def __load_API_headers(self):
        self.PLT_HEADER = config['API_headers']['plt']
        self.XXL_HEADER = config['API_headers']['xxl']
        self.CS_HEADER = config['API_headers']['cs']
        self.CS_SECRET = config['secret']['cs_secret']
        self.PLT_SECRET = config['secret']['plt_secret']

    def __load_mongo(self):
        if os.getenv('MODE') is None:
            self.MONGO_PLT_HOST = config['mongo_connection']['mongo_plt_host']
            self.MONGO_CS_HOST = config['mongo_connection']['mongo_cs_host']
            self.MONGO_PLT_ACCOUNT = config['mongo_connection']['mongo_plt_account']
            self.MONGO_CS_ACCOUNT = config['mongo_connection']['mongo_cs_account']
            self.MONGO_PLT_PASSWORD = config['mongo_connection']['mongo_plt_password']
            self.MONGO_CS_PASSWORD = config['mongo_connection']['mongo_cs_password']
        else:
            self.MONGO_PLT_HOST = os.getenv('MONGO_PLT_HOST')
            self.MONGO_CS_HOST = os.getenv('MONGO_CS_HOST')
            self.MONGO_PLT_ACCOUNT = os.getenv('MONGO_PLT_ACCOUNT')
            self.MONGO_CS_ACCOUNT = os.getenv('MONGO_CS_ACCOUNT')
            self.MONGO_PLT_PASSWORD = os.getenv('MONGO_PLT_PASSWORD')
            self.MONGO_CS_PASSWORD = os.getenv('MONGO_CS_PASSWORD')

class GetClassData:

    def get_function_args(func):
        sig = inspect.signature(func)
        args = [param.name for param in sig.parameters.values()]
        return args