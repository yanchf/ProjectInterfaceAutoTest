A.简要介绍

    1.该项目对外提供两种excel文件，分别是位于./testcase_data/excel 下的test_*.xlsx文件，./testcase_data/env 下的env.xlsx
        a.testcase_data/excel/test_*.xlsx 存储测试接口相关数据
        b.testcase_data/env/env.xlsx 存储测试接口相关环境变量
    2.运行项目后，可以对 testcase_data/excel/ 文件夹 下一个或者多个 testcase_*.xlsx文件 中记录的接口进行简单的连通性测试（只测试该调用接口是否响应码为200）
    3.运行完成后将：
        生成运行日志.log
        钉钉通知对应调用的钉钉机器人，报告接口测试集中是否有调用失败的接口
        生成一份测试报告

B.使用方法

    1.安装Python 
    2.安装pip 工具
    3.更换pip源
    4.再根目录下打开cmd，输入pip install -r requirements.txt。初始化项目环境
    5.依照testcase_data/excel/testcase_模板.xlsx 创建文件
    6.参考testcase_data/excel/env.xlsx 文件输入测试运行环境
    7.在cmd界面中输入run_test.py 或者 python run_test.py 运行项目
    
    
C.*要点须知

    1.testcase_data/excel/testcase_*.xlsx 中有第一个工作表init_token存放登录相关接口信息
        超级码3.0系统一般登录流程是
            1.登录
            2.绑定企业
            3.绑定系统
        第一个工作表严格按照login/org/sys接口顺序输入数据

    2.testcase_data/excel/testcase_*.xlsx 中有第二个工作表testcase_data存放将要进行接口测试的相关数据
        name: 自定义接口名
        method:该接口请求方法
        api: 接口部分url，除去了协议和域名部分
        params:一般是get请求的入参，有则输入，无则置空
        json_data:一般是post请求的入参，当入参为json字符串时输入
        x_www_form_urlencoded_data：一般是post请求的入参，当入参为表单数据时输入

    3.testcase_data/env/env.xlsx 存放解释系统的正式/测试环境 协议+域名部分
        project_name：要求和testcase_data/excel/ 文件下项目 对应文件名一样
            例如：testcase_data/excel/testcase_longjin.xlsx 这时env.xlsx中一定要有
                testcase_longjin系统对应的测试环境 和正式环境的 域名

    4.config/config_file.py 中可以对钉钉机器人相关信息进行定义

    5.pytest.ini 文件可以对pytest框架命令行相关信息进行定义
        --html:生成测试报告 html格式
        --reruns * --reruns-delay *：失败重跑定义
        -n ：多线程执行定义

    6.loggin文件夹下存放运行日志相关信息
    7.report存放接口测试报告
    8.运行run_test.py是可以选择测试环境或正式环境，例如
        pytest run_test.py -r 传入"-r"参数可进行正式环境接口的测试
        默认不输入-r 将进行测试环境的接口测试
    9.不要进行包含动态参数的接口测试
    10.不要进行登录流程非3.0系统类型的接口测试
    
        
    
D.额外事项

    1.不同系统获取token方式不同，如果需要套用到 有其他获取token方式的系统，需要重写common/testcase_data_util.py文件
    2.建议集成jenkins 建立接口自动化测试项目
    3.建议扩展allure插件，生成美观的测试报告
    4.钉钉机器人只能调用 加签类型，且通知文案采用预置
    5.因为init_token只有一套账号，最好这个账号可以在测试环境和正式环境都能登录。不然会有一个环境无法初始化token而报错
    6.如果在testcase_data/excel 中加入多个项目的excel文件，程序将变得不稳定

    