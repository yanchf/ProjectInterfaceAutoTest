import pytest
from common.testcase_data_util import *
from common.loggin_util import LoggingUtil
from common.request_util import RequestUtil
from datetime import datetime
from py.xml import html


def _init_testcases() -> dict:
    print("测试用例:", get_testcases())
    return get_testcases()


# 初始化测试用例名字：项目名+接口名
def _init_testcase(fixture_value):
    return fixture_value["project"] + " - " + fixture_value["name"]


# 初始化所有接口测试用例
@pytest.fixture(params=_init_testcases(), ids=_init_testcase)
def init_testcase(request):
    return request.param


# 初始化日志记录工具
@pytest.fixture(scope="class")
def init_loggingutil():
    logging_util_temp = LoggingUtil(__name__)
    logging_util = logging_util_temp.init_logger()

    return logging_util


# 实例化请求工具
@pytest.fixture(scope="class")
def init_request_util():
    request_util = RequestUtil()
    return request_util


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
    cells.pop()
