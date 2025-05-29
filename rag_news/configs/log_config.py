#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/05/19 20:45:04
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment
"""

# 定义统一的日志格式
import os
import sys
from loguru import logger


# 存储已创建的logger实例，避免重复创建
_LOGGERS = {}


class LogConfig(object):
    """日志配置类"""

    # 基本日志格式
    LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss}|{file} -- {name}:{function}:{line} | {level} | {message}"

    # 日志目录
    LOG_DIR = "logs"

    # 日志文件大小限制
    LOG_SIZE = "10 MB"

    # 保留的日志文件数量
    LOG_ROTATION = 10

    # 压缩旧日志
    LOG_COMPRESSION = "zip"

    # 标记是否已初始化
    _initialized = False

    @classmethod
    def setup(cls):
        """设置日志目录"""
        # 创建日志目录
        os.makedirs(cls.LOG_DIR, exist_ok=True)

        # 只在第一次调用时移除默认处理器
        if not cls._initialized:
            logger.remove()
            cls._initialized = True

    @classmethod
    def get_logger(cls, name):
        """
        获取指定名称的日志记录器

        Args:
            name: 日志记录器名称，通常是模块名

        Returns:
            配置好的logger对象
        """
        # 如果已经创建过这个名称的logger，直接返回缓存的实例
        if name in _LOGGERS:
            return _LOGGERS[name]

        # 确保日志目录存在并初始化
        cls.setup()

        # 创建新的logger实例
        named_logger = logger.bind(name=name)

        # 添加控制台输出
        # 使用过滤器确保只处理对应名称的日志
        named_logger.add(
            sys.stderr,
            format=cls.LOG_FORMAT,
            level="INFO",
            filter=lambda record: record["extra"].get("name") == name,
            enqueue=True,
        )

        # 添加文件输出
        log_file = os.path.join(cls.LOG_DIR, f"{name}.log")
        named_logger.add(
            log_file,
            format=cls.LOG_FORMAT,
            level="DEBUG",
            rotation=cls.LOG_SIZE,
            retention=cls.LOG_ROTATION,
            compression=cls.LOG_COMPRESSION,
            filter=lambda record: record["extra"].get("name") == name,
            enqueue=True,  # 线程安全
        )

        # 缓存这个logger实例
        _LOGGERS[name] = named_logger

        return named_logger


data_logger = LogConfig.get_logger("data")
model_logger = LogConfig.get_logger("model")
main_logger = LogConfig.get_logger("main")
