#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/10 17:10:57
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
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
    rotation: str = "1 hour"
    retention: str = "30 days"
    serialize: bool = False
    module_specific_logs: bool = False
    modules_log_dir: Path = PROJECT_ROOT / "logs/modules"
    enable_console: bool = True  # 是否启用控制台输出


def format_extra(record):
    """格式化 extra 字典"""
    if record["extra"] and any(record["extra"].values()):
        extra_parts = [f"{k}={v}" for k, v in record["extra"].items() if v]
        return " | " + ", ".join(extra_parts) if extra_parts else ""
    return ""


def add_handlers(logger_instance, config: LogConfig, app_name: str, env: str, 
                log_dir: Path = None, module_filter: str = None, only_errors: bool = False):
    """统一添加日志处理器的函数"""
    console_level = os.getenv("LOG_CONSOLE_LEVEL", config.console_level)
    file_level = os.getenv("LOG_FILE_LEVEL", config.file_level)
    log_directory = log_dir or config.log_dir
    
    # 检查是否启用控制台输出
    enable_console = config.enable_console
    # 环境变量可以覆盖配置
    if os.getenv("LOG_ENABLE_CONSOLE") is not None:
        enable_console = os.getenv("LOG_ENABLE_CONSOLE").lower() in ["true", "1", "yes"]
    
    # 生产环境默认不输出到控制台（除非明确启用）
    if env == "prod" and os.getenv("LOG_ENABLE_CONSOLE") is None:
        enable_console = False
    
    # 确保日志目录存在
    log_directory.mkdir(exist_ok=True, parents=True)
    
    # 创建过滤器
    def create_filter(private_only=False, module_name=None, errors_only=False):
        def filter_func(record):
            # 私有日志过滤
            is_private = record["extra"].get("_private_log") is True
            if private_only and not is_private:
                return False
            if not private_only and is_private:
                return False
            
            # 模块过滤
            if module_name and record["extra"].get("module") != module_name:
                return False
            
            # 错误级别过滤
            if errors_only and record["level"].name not in ["ERROR", "CRITICAL"]:
                return False
                
            return True
        return filter_func
    
    handler_ids = []
    
    # 添加控制台处理器（根据配置决定是否添加）
    if not only_errors and enable_console:
        console_id = logger_instance.add(
            sys.stderr,
            level=console_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level><level> {extra_str} </level>",
            colorize=True,
            filter=create_filter(private_only=bool(module_filter), module_name=module_filter)
        )
        handler_ids.append(console_id)
    
    # 添加文件处理器
    if not only_errors:
        log_path = log_directory / f"{app_name}_{env}.log"
        file_id = logger_instance.add(
            str(log_path),
            level=file_level,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} {extra_str}",
            rotation=config.rotation,
            retention=config.retention,
            serialize=config.serialize,
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
            filter=create_filter(private_only=bool(module_filter), module_name=module_filter)
        )
        handler_ids.append(file_id)
    
    # 生产环境或指定错误日志
    if env == "prod" or only_errors:
        error_log_path = log_directory / f"{app_name}_{env}_errors.log"
        error_id = logger_instance.add(
            str(error_log_path),
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} {extra_str}",
            rotation=config.rotation,
            retention=config.retention,
            filter=create_filter(private_only=bool(module_filter), module_name=module_filter, errors_only=True),
            backtrace=True,
            diagnose=True,
        )
        handler_ids.append(error_id)
    
    return handler_ids


def setup_logger(config: LogConfig = None, app_name: str = "app", env: str = None):
    """配置并返回logger实例"""
    if config is None:
        config = LogConfig()
    
    env = env or os.getenv("APP_ENV", "dev")
    
    # 移除默认处理器并配置格式化器
    _logger.remove()
    _logger.configure(patcher=lambda record: record.update(extra_str=format_extra(record)))
    
    # 添加处理器
    add_handlers(_logger, config, app_name, env)
    
    return _logger


def get_module_logger(name: str, output_to_file: bool = False, only_file: bool = False,
                     log_dir: Path = None, config: LogConfig = None, env: str = None):
    """获取模块专用logger"""
    if config is None:
        config = LogConfig()
    
    env = env or os.getenv("APP_ENV", "dev")
    module_log_dir = log_dir or config.modules_log_dir
    
    if output_to_file and only_file:
        # 只输出到独立文件
        module_logger = _logger.bind(module=name, _private_log=True)
        add_handlers(_logger, config, name, env, module_log_dir, module_filter=name)
    elif output_to_file:
        # 输出到主日志和独立文件
        module_logger = _logger.bind(module=name)
        add_handlers(_logger, config, name, env, module_log_dir, module_filter=name)
    else:
        # 只输出到主日志
        module_logger = _logger.bind(module=name)
    
    return module_logger


# 创建默认logger实例
logger = setup_logger(env="dev")


def log_exception(func):
    """记录函数异常的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"函数 {func.__name__} 执行失败: {e}")
            raise
    return wrapper


if __name__ == "__main__":
    from pathlib import Path

    # logger.info("test")

    specific_logger = get_module_logger(
        name="web_crawler", 
        output_to_file=True,
        only_file=True,  # 关键参数：只输出到专用文件夹
        log_dir=Path("./logs/test")
    )

    specific_logger.info("test")