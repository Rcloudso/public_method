"""
浏览器配置模块
集中管理各种浏览器的配置选项
"""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class BrowserConfig:
    """浏览器配置类，管理不同浏览器的启动选项"""

    def __init__(self):
        self.user_data_dir = os.getenv('CHROME_USER_DATA_DIR', 
                                       str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default"))

    def get_chrome_options(self, headless=False, mobile=False, with_cache=False):
        """
        获取Chrome浏览器配置选项
        
        Args:
            headless: 是否启用无头模式
            mobile: 是否启用移动模式
            with_cache: 是否使用缓存
            
        Returns:
            配置好的ChromeOptions实例
        """
        options = ChromeOptions()
        
        # 通用配置
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # 添加实验性选项
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0,
            "download.prompt_for_download": False
        }
        options.add_experimental_option('prefs', prefs)
        
        # 禁用自动化提示
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 为移动设备配置
        if mobile:
            mobile_emulation = {"deviceName": "iPhone X"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # 无头模式配置
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        
        # 用户数据目录配置
        if with_cache:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
        
        return options
    
    def get_firefox_options(self, headless=False):
        """
        获取Firefox浏览器配置选项
        
        Args:
            headless: 是否启用无头模式
            
        Returns:
            配置好的FirefoxOptions实例
        """
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        
        # 设置下载行为
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                              "application/x-gzip,application/zip,application/x-zip-compressed")
        
        return options
    
    def get_edge_options(self, headless=False):
        """
        获取Edge浏览器配置选项
        
        Args:
            headless: 是否启用无头模式
            
        Returns:
            配置好的EdgeOptions实例
        """
        options = EdgeOptions()
        
        # 通用配置
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        # 禁用自动化提示
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        # 无头模式配置
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        
        return options 