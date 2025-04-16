"""
登录功能测试用例
使用pytest框架测试登录功能
"""
import pytest
from typing import Dict, Any

from pages.login_page import LoginPage
from utils.logger import default_logger as logger


@pytest.mark.functional
class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.smoke
    def test_valid_login(self, driver, config: Dict[str, Any]):
        """测试有效用户登录"""
        # 从配置中获取测试数据
        username = config["test_data"]["username"]
        password = config["test_data"]["password"]
        
        # 创建登录页面对象
        login_page = LoginPage(driver)
        
        # 执行登录
        is_login_successful = login_page.login(username, password)
        
        # 断言登录成功
        assert is_login_successful, "登录失败"
        
        # 检查URL变化（已导航到主页）
        current_url = driver.current_url
        assert "login" not in current_url.lower(), f"登录后URL仍然在登录页: {current_url}"
    
    @pytest.mark.parametrize("username, password, expected_error", [
        ("invalid_user", "invalid_pass", "用户名或密码错误"),
        ("", "password123", "请输入用户名"),
        ("test_user", "", "请输入密码"),
    ])
    def test_invalid_login(self, driver, username: str, password: str, expected_error: str):
        """测试无效登录场景"""
        # 创建登录页面对象
        login_page = LoginPage(driver)
        
        # 执行登录
        is_login_successful = login_page.login(username, password)
        
        # 断言登录失败
        assert not is_login_successful, "非法登录信息居然成功了"
        
        # 检查错误消息
        error_message = login_page.get_error_message()
        assert expected_error in error_message, f"错误消息不符合预期。实际: {error_message}, 预期: {expected_error}"
    
    def test_remember_me(self, driver, config: Dict[str, Any]):
        """测试记住我功能"""
        # 从配置中获取测试数据
        username = config["test_data"]["username"]
        password = config["test_data"]["password"]
        
        # 创建登录页面对象
        login_page = LoginPage(driver)
        
        # 检查默认情况下记住我是否未选中
        assert not login_page.is_remember_me_checked(), "记住我选项默认已选中"
        
        # 执行登录并勾选记住我
        login_page.login(username, password, remember_me=True)
        
        # 关闭浏览器并重新打开，检查是否自动登录（这部分在实际测试中要单独处理）
        logger.info("记住我功能测试完成")
    
    def test_forgot_password(self, driver):
        """测试忘记密码链接"""
        # 创建登录页面对象
        login_page = LoginPage(driver)
        
        # 点击忘记密码链接
        login_page.click_forgot_password()
        
        # 等待页面加载
        login_page.wait_for_page_load()
        
        # 验证已导航到密码重置页面
        current_url = driver.current_url
        assert "reset" in current_url.lower() or "forgot" in current_url.lower(), "未导航到密码重置页面" 