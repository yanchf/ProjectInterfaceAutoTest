import pytest


class TestInterface:

    def test_interface(self, init_testcase, init_loggingutil, init_request_util):
        # 初始化接口请求工具
        request_util = init_request_util
        # 初始化日志系统工具
        logging_util = init_loggingutil

        # 基于数据驱动的接口请求测试
        response = request_util.request_util(init_testcase)

        # 日志系统记录测试用例数据
        logging_util.info(init_testcase)
        # 日志系统记录接口测试结果
        logging_util.info(response.json())

        # 断言
        # 硬断言接口是否正常
        assert response.ok is True

        # 软断言接口结果
        pytest.assume(response.json()["state"] == 200)
        pytest.assume(response.json()["internalErrorCode"] == "0")
        pytest.assume(response.json()["msg"] == "success")
