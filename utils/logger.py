"""
日志模块
提供统一的日志记录功能
"""
import os
import sys
import time
import functools
from datetime import datetime
from pathlib import Path
from typing import Callable, Any
from loguru import logger


class Logger:
    """日志管理类，封装loguru库提供更简单的使用方式"""

    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名 (logs/YYYY-MM-DD.log)
        log_file = Path(log_dir) / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # 配置日志格式
        fmt = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>")
        
        # 清除默认处理器
        logger.remove()
        
        # 添加控制台处理器
        logger.add(
            sys.stderr,
            format=fmt,
            level="INFO",
            colorize=True
        )
        
        # 添加文件处理器
        logger.add(
            str(log_file),
            format=fmt,
            level="DEBUG",
            rotation="500 MB",  # 日志文件大小达到500MB时轮转
            retention="10 days",  # 保留10天的日志
            compression="zip",  # 压缩旧日志
            encoding="utf-8"
        )
        
        # 添加错误日志处理器
        error_log_file = Path(log_dir) / f"error_{datetime.now().strftime('%Y-%m-%d')}.log"
        logger.add(
            str(error_log_file),
            format=fmt,
            level="ERROR",
            rotation="100 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            filter=lambda record: record["level"].name == "ERROR"
        )
    
    def get_logger(self):
        """获取logger实例"""
        return logger


def log_time(func: Callable) -> Callable:
    """
    装饰器：记录函数执行时间
    
    用法:
        @log_time
        def example_function():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.debug(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
            return result
        except Exception as e:
            end_time = time.time()
            logger.error(f"函数 {func.__name__} 执行失败，用时: {end_time - start_time:.4f}秒, 错误: {e}")
            raise
    return wrapper


# 创建默认日志实例
default_logger = Logger().get_logger() 