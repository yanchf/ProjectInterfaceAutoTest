import logging
from logging import handlers
import datetime
import os


# 日志工具封装
class LoggingUtil:

    def __init__(self, logger_name, logger_level=10):
        self.logger = None
        self.logger_name = logger_name
        if logger_level in [10, 20, 30, 40, 50]:
            self.logger_level = logger_level
        else:
            raise TypeError("初始化日志等级入参错误")

    def init_logger(self):

        if not ('loggin' in os.listdir()):
            os.mkdir(r"./loggin")
        if not ('report' in os.listdir()):
            os.mkdir(r"./report")

        # 创建格式化器
        console_fmt = r"%(asctime)s - %(levelname)8s - %(filename)10s:%(lineno)4s - %(message)s"
        console_data = r"%Y-%m-%d %H:%M:%S"
        file_fmt = r"%(asctime)-25s - %(name)s:%(levelname)-8s: %(levelno)-2s - funcName:%(funcName)15s  - %(message)-1000s" \
                   r" -- pathname:%(pathname)s - filename:%(filename)-20s - module:%(module)-15s  lineno:%(lineno)-4d" \
                   r" - created:%(created)-5f  msecs:%(msecs)-5d  relativeCreated:%(relativeCreated)-5d  thread:%(thread)-5d  threadName:%(threadName)-10s  process:%(process)-5d"

        # 个人邮箱smtp配置参数
        smtp_config = {
            "mailhost": ("smtp.qq.com", 25),
            "fromaddr": "1847572557@qq.com",
            "toaddrs": "1847572557@qq.com",
            "subject": "ERROR_LOG",
            "credentials": ("1847572557@qq.com", "password"),
            "secure": None,
            "timeout": 1.0
        }

        console_formatter = logging.Formatter(fmt=console_fmt, datefmt=console_data)
        file_formatter = logging.Formatter(fmt=file_fmt)

        # 创建处理器 & 关联处理器和格式化器
        console_handler = logging.StreamHandler()
        file_handler = handlers.RotatingFileHandler(
            filename=r"./loggin/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log",
            mode="a", encoding="utf8")

        smtp_handler = handlers.SMTPHandler(**smtp_config)
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 设置处理器接受日志等级
        console_handler.setLevel(logging.WARNING)
        file_handler.setLevel(logging.DEBUG)
        smtp_handler.setLevel(logging.CRITICAL)

        # 创建记录器 & 关联记录器和处理器
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logger_level)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(smtp_handler)

        return self.logger
