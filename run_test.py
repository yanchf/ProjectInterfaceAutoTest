import argparse
from datetime import datetime
import pytest
from common.loggin_util import LoggingUtil
from common.ddrobot_util import pytest_result_code

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-r", "--real", help="正式环境标记", action="store_false")
arg = parser.parse_args()

# 传入参数决定测试环境是 正式还是测试，默认测试
if arg.real:
    arg_env = "test_env"
else:
    arg_env = "real_env"

if __name__ == "__main__":

    now = datetime.now().strftime("%Y-%m-%d %H_%M_%S")

    # 初始化日志工具，记录程序运行状态
    logging_util_temp = LoggingUtil(__name__)
    logging_util = logging_util_temp.init_logger()

    # 运行自动化程序
    try:
        # 日志记录测试环境是正式环境还是测试环境
        logging_util.info(arg_env)
        result = pytest.main(["--html=report/" + now + "_report.html"])
        # 日志记录pytest运行结果
        logging_util.info(result)
        # 根据结果调用钉钉机器人
        pytest_result_code(result)
    except Exception as e:
        # try语句块抛出异常程序执行出现异常
        print("接口自动化运行错误", e, "\n")
        logging_util.exception(e)

    else:
        # try语句块执行无异常
        ...
