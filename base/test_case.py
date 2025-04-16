"""
测试工具类
提供所有测试用例的通用方法和函数
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from utils.logger import default_logger as logger


class TestHelper:
    """
    测试辅助工具类
    提供通用的测试辅助方法，用于配合pytest fixtures使用
    """
    
    @staticmethod
    def take_screenshot(driver: WebDriver, name: Optional[str] = None, 
                      screenshot_dir: str = "screenshots") -> str:
        """
        截取当前页面截图
        
        Args:
            driver: WebDriver实例
            name: 自定义截图名称，如不提供则使用时间戳
            screenshot_dir: 截图保存目录
            
        Returns:
            截图文件路径
        """
        # 创建截图目录
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = name or f"screenshot_{timestamp}"
        
        if not name.endswith(".png"):
            name += ".png"
            
        filepath = str(Path(screenshot_dir) / name)
        
        try:
            driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    @staticmethod
    def navigate_to(driver: WebDriver, url: str) -> None:
        """
        导航到指定URL
        
        Args:
            driver: WebDriver实例
            url: 目标URL
        """
        try:
            driver.get(url)
            logger.info(f"导航到页面: {url}")
        except Exception as e:
            logger.error(f"导航失败: {e}")
            raise
    
    @staticmethod
    def get_current_url(driver: WebDriver) -> str:
        """获取当前URL"""
        return driver.current_url
    
    @staticmethod
    def get_page_title(driver: WebDriver) -> str:
        """获取当前页面标题"""
        return driver.title 