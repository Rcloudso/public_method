"""
Pytest配置文件
提供测试环境设置和自定义夹具(fixtures)
"""
import os
import json
import pytest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from selenium.webdriver.remote.webdriver import WebDriver

from base.browser_driver import BrowserFactory
from utils.logger import default_logger as logger
from utils.config_reader import ConfigReader


# 添加命令行选项
def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption("--browser", action="store", default="chrome",
                     help="指定浏览器类型: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", default=False,
                     help="启用无头模式")
    parser.addoption("--env", action="store", default="test",
                     help="指定测试环境: dev, test, stage, prod")
    parser.addoption("--mobile", action="store_true", default=False,
                     help="启用移动设备模拟")


# 全局夹具，提供WebDriver实例
@pytest.fixture(scope="function")
def driver(request) -> WebDriver:
    """
    提供WebDriver实例的夹具
    
    用法:
        def test_example(driver):
            driver.get("https://www.example.com")
    """
    # 从命令行参数获取配置
    browser_type = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    mobile = request.config.getoption("--mobile")
    
    # 创建WebDriver实例
    driver = BrowserFactory.create_driver(
        browser_type=browser_type,
        headless=headless,
        mobile=mobile
    )
    
    logger.info(f"初始化 {browser_type} 浏览器 {'(headless)' if headless else ''} {'(mobile)' if mobile else ''}")
    
    # 返回WebDriver实例并在测试结束后关闭
    yield driver
    
    # 关闭浏览器
    driver.quit()
    logger.info("浏览器已关闭")


# 配置夹具，提供测试配置
@pytest.fixture(scope="session")
def config(request) -> Dict[str, Any]:
    """
    提供测试配置的夹具
    
    用法:
        def test_example(config):
            base_url = config["base_url"]
    """
    # 获取当前环境
    env = request.config.getoption("--env")
    
    # 加载对应环境的配置文件
    config_file = f"config/{env}.yaml"
    
    # 如果配置文件不存在，使用默认配置
    if not Path(config_file).exists():
        logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
        config_data = {
            "base_url": "https://localhost",
            "api_url": "https://localhost/api",
            "timeout": 10,
            "credentials": {
                "username": "test",
                "password": "test"
            }
        }
    else:
        # 读取配置文件
        config_data = ConfigReader.load_yaml(config_file)
        logger.info(f"已加载配置: {env}")
    
    return config_data


# 测试报告夹具
@pytest.fixture(scope="session", autouse=True)
def configure_html_report_env(request):
    """配置HTML报告的环境信息"""
    config = request.config
    
    # 添加环境信息到HTML报告
    env_data = {
        "Browser": request.config.getoption("--browser"),
        "Headless": str(request.config.getoption("--headless")),
        "Environment": request.config.getoption("--env"),
        "Mobile": str(request.config.getoption("--mobile")),
        "Python": os.sys.version,
        "OS": os.name
    }
    
    # 创建环境文件
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    with open(reports_dir / "environment.json", "w") as f:
        json.dump(env_data, f, indent=2)


# 截图夹具
@pytest.fixture(scope="function")
def take_screenshot(driver):
    """
    提供截图功能的夹具
    
    用法:
        def test_example(driver, take_screenshot):
            driver.get("https://www.example.com")
            take_screenshot("homepage")
    """
    
    def _take_screenshot(name=None):
        """
        截取当前页面的截图
        
        Args:
            name: 截图文件名，如不提供则使用时间戳
        
        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = name or f"screenshot_{timestamp}"
        
        if not name.endswith(".png"):
            name += ".png"
        
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        filepath = str(screenshots_dir / name)
        
        try:
            driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    return _take_screenshot


# 自动截图失败的测试
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行后的钩子函数，用于失败时自动截图"""
    # 执行测试
    outcome = yield
    rep = outcome.get_result()
    
    # 我们只关心实际测试阶段的失败
    if rep.when == "call" and rep.failed:
        # 尝试获取当前测试的WebDriver实例
        driver = item.funcargs.get("driver", None)
        
        # 如果找到了WebDriver，则截图
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"fail_{item.name}_{timestamp}.png"
            
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            filepath = str(screenshots_dir / name)
            
            try:
                driver.save_screenshot(filepath)
                logger.info(f"测试失败截图已保存: {filepath}")
            except Exception as e:
                logger.error(f"截图失败: {e}") 