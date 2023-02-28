import time
import hmac
import hashlib
import base64
import urllib.parse
import argparse
from datetime import datetime

import requests

from config import config_file


def _get_secret_url():
    # 第一步，
    # 把timestamp+"\n"+密钥当做签名字符串，
    # 使用HmacSHA256算法计算签名，
    # 然后进行Base64 encode，
    # 最后再把签名参数再进行urlEncode，
    # 得到最终的签名（需要使用UTF-8字符集）。

    timestamp = str(round(time.time() * 1000))
    secret = config_file.dd_secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    # 第二步，把 timestamp和第一步得到的签名值拼接到URL中。
    secret_url = config_file.dd_robot_webhook + "?" + "access_token=" + config_file.dd_robot_access_token[
        "access_token"] + "&" + "timestamp=" + timestamp + "&" + "sign=" + sign

    return secret_url


def dingding(result, now_time, report_image_path=None, log_path=None):
    url = _get_secret_url()

    # print(payload)

    # 第三步，发送消息text类型或者link类型、markdown类型、跳转ActionCard类型
    # body = {
    #     "msgtype": "text",
    #     "text": {
    #         "content": "测试不通过，接口名称：%s" % api_name
    #     },
    #     "at": {
    #         "atMobiles": [
    #         ],
    #         "isAtAll": False
    #     }
    # }

    # logging_util_temp = LoggingUtil(__name__)
    # logging_util = logging_util_temp.init_logger()

    dd_content = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": now_time + "接口自动化",
            "text": "测试结果： {result} \n\n ![screenshot]({report_image}) \n\n 时间：{result_time}",
            "btnOrientation": "0",
            "btns": [
                {
                    "title": "测试报告.png",
                    "actionURL": None
                },
                {
                    "title": "运行日志.log",
                    "actionURL": None
                }
            ]
        }
    }

    dd_content["actionCard"]["text"] = dd_content["actionCard"]["text"].format(result=result,
                                                                               report_image=report_image_path,
                                                                               result_time=now_time)
    dd_content["actionCard"]["btns"][0]["actionURL"] = r"file://" + str(report_image_path)
    dd_content["actionCard"]["btns"][1]["actionURL"] = r"file://" + str(log_path)

    response = requests.post(url=url, headers=config_file.dd_robot_headers, json=dd_content)
    # logging_util.debug(response.text)


def error_dingding(atMobiles=None, atUserIds=None):
    url = _get_secret_url()

    dd_error_content = {
        "at": {
            "atMobiles": [
                atMobiles
            ],
            "atUserIds": [
                atUserIds
            ],
            "isAtAll": False
        },
        "text": {
            "content": "接口自动化测试 - 执行结果异常!!!"
        },
        "msgtype": "text"
    }

    response = requests.post(url=url, headers=config_file.dd_robot_headers, json=dd_error_content)
    # logging_util.debug(response.text)


def pytest_result_code(code: int):
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if code == 1:
        dingding("接口自动化测试：失败，退出码为1", now_time=now_time)
        error_dingding()
        print("error_dingding")
    elif code == 0:
        dingding("接口自动化测试：成功，退出码为0", now_time=now_time)
    else:
        dingding(("退出码%s" % code), now_time=now_time)
        error_dingding()
        print("退出码%s" % code)
        raise TypeError("自动化程序退出码未知")


if __name__ == '__main__':
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    args = parser.parse_args()

    if args.result == '1':
        dingding("接口测试：失败，退出码为1", now)
        error_dingding()
        print("error_dingding")
    elif args.result == '0':
        dingding("接口测试：成功，退出码为0", now)
    else:
        dingding(("退出码%s" % args.result), now)
        error_dingding()
        print("退出码%s" % args.result)
        raise TypeError("自动化程序退出码未知")
