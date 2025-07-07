#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @File    :   logging.py
#          @Time    :   2025/07/07 15:10:54
#          @Author  :   heng
#          @Version :   1.0
#          @Contact :   hengsblog@163.com
#          @Copyright (c) 2025 Baidu.com, Inc. All Rights Reserved
###############################################################
"""
@comment: 日志配置
"""

import os
import sys
from enum import Enum
from pathlib import Path

from loguru import logger as _logger
from pydantic import BaseModel

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogConfig(BaseModel):
    """日志配置模型"""
    console_level: LogLevel = LogLevel.INFO
    file_level: LogLevel = LogLevel.DEBUG
    log_dir: Path = PROJECT_ROOT / "logs"
    rotation: str = "10 MB"  # 文件大小轮转
    retention: str = "30 days"  # 日志保留时间
    serialize: bool = False  # 是否序列化为JSON
    module_specific_logs: bool = False  # 是否启用模块特定日志
    modules_log_dir: Path = PROJECT_ROOT / "logs/modules"  # 模块日志目录

class ExtraFormatter:
    """格式化 extra 字典，如果为空则返回空字符串"""
    def __call__(self, record):
        if record["extra"] and any(record["extra"].values()):
            # 构建格式化的 extra 字符串
            extra_parts = []
            for key, value in record["extra"].items():
                if value:  # 只添加非空值
                    extra_parts.append(f"{key}={value}")
            
            if extra_parts:
                return " | " + ", ".join(extra_parts)
        return ""  # 如果 extra 为空，返回空字符串


def setup_logger(
    config: LogConfig = None,
    app_name: str = "app",
    env: str = None
) -> _logger.__class__:
    """
    配置并返回logger实例

    Args:
        config: 日志配置
        app_name: 应用名称
        env: 环境名称(dev, test, prod)
    """
    if config is None:
        config = LogConfig()

    # 获取环境变量
    env = env or os.getenv("APP_ENV", "dev")
    console_level = os.getenv("LOG_CONSOLE_LEVEL", config.console_level)
    file_level = os.getenv("LOG_FILE_LEVEL", config.file_level)

    # 确保日志目录存在
    config.log_dir.mkdir(exist_ok=True, parents=True)

    # 移除默认处理器
    _logger.remove()

    # 修改所有处理器的格式字符串，使用 record["extra_str"] 替代 {extra}
    _logger.configure(patcher=lambda record: record.update(extra_str=ExtraFormatter()(record)))
    # 添加控制台处理器
    _logger.add(
        sys.stderr,
        level=console_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level><level> {extra_str} </level>",
        colorize=True,
    )

    # 修改这里：使用日期时间格式作为文件名的一部分，但不包含分钟和秒
    # 设置rotation="1 hour"进行每小时轮转
    log_path = config.log_dir / f"{app_name}_{env}.log"

    # 添加文件处理器，设置按小时轮转
    _logger.add(
        str(log_path),
        level=file_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} {extra_str}",
        rotation="1 hour",  # 每小时轮转一次
        retention=config.retention,
        serialize=config.serialize,
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    # 生产环境错误日志也使用同样的按小时轮转
    if env == "prod":
        error_log_path = config.log_dir / f"{app_name}_{env}_errors.log"
        _logger.add(
            str(error_log_path),
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="1 hour",  # 每小时轮转一次
            retention=config.retention,
            filter=lambda record: record["level"].name == "ERROR" or record["level"].name == "CRITICAL",
            backtrace=True,
            diagnose=True,
        )

    return _logger


# 创建默认logger实例
logger = setup_logger(env='dev')


def get_module_logger(name: str):
    """获取模块专用logger"""
    module_logger = _logger.bind(module=name)
    return module_logger


# 异常捕获装饰器
def log_exception(func):
    """记录函数异常的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"函数 {func.__name__} 执行失败: {e}")
            raise
    return wrapper
