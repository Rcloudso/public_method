"""
浏览器驱动管理模块
支持多种浏览器和自动下载管理驱动
"""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.browser_config import BrowserConfig
from utils.logger import default_logger as logger


class BrowserFactory:
    """浏览器工厂类，负责创建各种浏览器实例"""
    
    # 缓存WebDriver管理器实例
    _driver_managers = {
        "chrome": None,
        "firefox": None,
        "edge": None
    }
    
    @classmethod
    def _get_driver_manager(cls, browser_type):
        """
        获取WebDriver管理器实例，使用缓存避免重复下载
        
        Args:
            browser_type: 浏览器类型
            
        Returns:
            对应的WebDriver管理器实例
        """
        if cls._driver_managers[browser_type] is None:
            if browser_type == "chrome":
                cls._driver_managers[browser_type] = ChromeDriverManager(cache_valid_range=7)
            elif browser_type == "firefox":
                cls._driver_managers[browser_type] = GeckoDriverManager(cache_valid_range=7)
            elif browser_type == "edge":
                cls._driver_managers[browser_type] = EdgeChromiumDriverManager(cache_valid_range=7)
        
        return cls._driver_managers[browser_type]
    
    @staticmethod
    def create_driver(browser_type="chrome", headless=False, mobile=False, with_cache=False):
        """
        创建并返回指定类型的WebDriver实例
        
        Args:
            browser_type: 浏览器类型 (chrome/firefox/edge)
            headless: 是否启用无头模式
            mobile: 是否启用移动模式
            with_cache: 是否使用缓存
            
        Returns:
            WebDriver实例
        """
        browser_type = browser_type.lower()
        browser_config = BrowserConfig()
        
        # 创建drivers目录用于存储驱动
        drivers_dir = Path("drivers")
        drivers_dir.mkdir(exist_ok=True)
        
        try:
            if browser_type == "chrome":
                options = browser_config.get_chrome_options(headless, mobile, with_cache)
                manager = BrowserFactory._get_driver_manager("chrome")
                driver = webdriver.Chrome(
                    service=ChromeService(manager.install()),
                    options=options
                )
            elif browser_type == "firefox":
                options = browser_config.get_firefox_options(headless)
                manager = BrowserFactory._get_driver_manager("firefox")
                driver = webdriver.Firefox(
                    service=FirefoxService(manager.install()),
                    options=options
                )
            elif browser_type == "edge":
                options = browser_config.get_edge_options(headless)
                manager = BrowserFactory._get_driver_manager("edge")
                driver = webdriver.Edge(
                    service=EdgeService(manager.install()),
                    options=options
                )
            else:
                raise ValueError(f"不支持的浏览器类型: {browser_type}")
            
            # 设置默认等待时间
            driver.implicitly_wait(10)
            logger.info(f"成功初始化 {browser_type} 浏览器 {'(headless)' if headless else ''}")
            return driver
        except Exception as e:
            logger.error(f"初始化浏览器失败: {e}")
            raise
