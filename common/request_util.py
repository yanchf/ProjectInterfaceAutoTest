import requests
import json
import common.testcase_data_util as testcase_data_util
from run_test import arg_env
from common.loggin_util import LoggingUtil


# requests的简单封装
class RequestUtil:
    # 设置单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __init__(self, env: str = 'test_env', init_token=False, **kwargs):
        self.session = requests.sessions.Session()
        # 这是命令行传参，决定当前是否正式/测试环境的参数
        self.env = arg_env
        self.kwargs = kwargs
        # 初始化系统测试环境
        self.env_dict = testcase_data_util.get_env()
        # 初始化系统token
        self.tokens = testcase_data_util.get_tokens()
        # 初始化日志系统
        logging_util_temp = LoggingUtil(__name__)
        self.logging_util = logging_util_temp.init_logger()
        # 日志系统记录初始化的系统测试环境和系统token以备查看
        self.logging_util.info(self.env_dict)
        self.logging_util.info(self.tokens)

        print("\n" * 2)
        print("控制台查看环境是否读取正确：", self.env_dict, "\n")
        print("控制台查看token是否初始化成功：", self.tokens, "\n")
        print("\n" * 2)

    def request_util(self, data: dict):
        # 根据对应项目名获得初始化token
        headers = {"super-token": self.tokens[data["project"]]}
        self.logging_util.info(headers)

        # data是个测试用例，以下代码是根据测试用例进行的接口请求
        if data["method"].upper() == "GET":
            if data["params"] is not None:
                url = self.env_dict[data["project"]][self.env] + data["api"] + "?" + data["params"]
            else:
                url = self.env_dict[data["project"]][self.env] + data["api"]
                
            self.logging_util.info(url)

            responses = self.session.request(method=data["method"], url=url, headers=headers, **self.kwargs)
        elif data["method"].upper() == "POST":
            if data["json_data"] is not None:
                url = self.env_dict[data["project"]][self.env] + data["api"]
                json_data = json.loads(data["json_data"])
                params_data = data["params"]

                self.logging_util.info(url)
                self.logging_util.info(data["json_data"])
                self.logging_util.info(data["params"])

                responses = self.session.request(method=data["method"], url=url, json=json_data, params=params_data, headers=headers, **self.kwargs)
            elif data["x_www_form_urlencoded_data"] is not None:
                url = self.env_dict[data["project"]][self.env] + data["api"]
                data_data = json.loads(data["x_www_form_urlencoded_data"])
                params_data = data["params"]

                self.logging_util.info(url)
                self.logging_util.info(data["x_www_form_urlencoded_data"])
                self.logging_util.info(data["params"])

                responses = self.session.request(method=data["method"], url=url, data=data_data, params=params_data, headers=headers, **self.kwargs)
            else:
                raise requests.exceptions.RequestException("不支持的传参类型")
        else:
            raise requests.exceptions.RequestException("不支持的请求方法")

        return responses
