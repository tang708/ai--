"""日志工具 — 单例 logger，同时输出到控制台和文件

文件按天轮转，存放于 log/YYYY-MM-DD.log
格式: 时间|级别|文件名|行号|消息
"""
import logging
import os.path
import time


class MyLogger:
    """自定义日志管理器，封装双通道日志输出"""

    def __init__(self):
        """初始化 logger：控制台 + 文件双通道，文件按天轮转"""
        self.logger = logging.getLogger("api_test")
        self.logger.setLevel(logging.DEBUG)

        # 控制台输出 INFO 及以上
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        # 文件输出 INFO 及以上，按天轮转
        file_name = "{}.log".format(time.strftime("%Y-%m-%d"))
        base_dir = os.path.dirname(__file__)
        log_dir = os.path.join(base_dir, "..", "log")
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        fh = logging.FileHandler(os.path.join(log_dir, file_name), encoding="utf-8")
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s|%(levelname)s|%(filename)s|%(lineno)s|%(message)s"
        )
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


# 模块级单例，所有模块共用
mylogger = MyLogger().logger
mylogger.info("日志模块初始化完成")
