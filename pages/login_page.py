"""
登录页面对象
演示页面对象模式的实现
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional

from base.page import BasePage
from utils.logger import default_logger as logger
from utils.encryption import Encryption


class LoginPage(BasePage):
    """登录页面类，封装登录页面的所有操作"""
    
    # 页面URL
    URL = "https://example.com/login"
    
    # 页面元素定位器
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    REMEMBER_ME = (By.ID, "remember-me")
    FORGOT_PASSWORD = (By.LINK_TEXT, "忘记密码?")
    
    def __init__(self, driver: WebDriver, url: Optional[str] = None):
        """
        初始化登录页面
        
        Args:
            driver: WebDriver实例
            url: 可选的自定义URL
        """
        super().__init__(driver, url or self.URL)
        logger.info("打开登录页面")
    
    def login(self, username: str, password: str, remember_me: bool = False) -> bool:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            remember_me: 是否勾选"记住我"
            
        Returns:
            登录是否成功
        """
        logger.info(f"尝试用户登录: {username}")
        
        # 输入用户名
        self.input_text(self.USERNAME_INPUT, username)
        
        # 输入密码
        self.input_text(self.PASSWORD_INPUT, password)
        
        # 勾选"记住我"
        if remember_me and not self.is_remember_me_checked():
            self.click(self.REMEMBER_ME)
        
        # 点击登录按钮
        self.click(self.LOGIN_BUTTON)
        
        # 等待页面加载
        self.wait_for_page_load()
        
        # 检查是否登录成功（URL变化或错误消息不存在）
        return not self.is_element_present(self.ERROR_MESSAGE, timeout=2)
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_remember_me_checked(self) -> bool:
        """
        检查"记住我"是否已勾选
        
        Returns:
            如果已勾选返回True，否则返回False
        """
        checkbox = self.find_element(self.REMEMBER_ME)
        return checkbox.is_selected()
    
    def click_forgot_password(self) -> None:
        """点击"忘记密码"链接"""
        self.click(self.FORGOT_PASSWORD)
        logger.info("点击忘记密码链接")
    
    def is_login_page_displayed(self) -> bool:
        """
        检查是否显示登录页面
        
        Returns:
            如果显示登录页面返回True，否则返回False
        """
        return (self.is_element_present(self.USERNAME_INPUT) and 
                self.is_element_present(self.PASSWORD_INPUT) and 
                self.is_element_present(self.LOGIN_BUTTON)) 