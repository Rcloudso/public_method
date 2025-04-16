"""
页面对象模型(POM)基类
提供所有页面对象的通用方法和属性
"""
import time
from typing import List, Optional, Union, Tuple, Any, Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from utils.logger import default_logger as logger


class BasePage:
    """
    页面对象基类
    所有页面类应继承此类以获取通用功能
    """
    
    def __init__(self, driver: WebDriver, url: Optional[str] = None):
        """
        初始化页面对象
        
        Args:
            driver: WebDriver实例
            url: 页面URL，如果提供则自动导航到该URL
        """
        self.driver = driver
        self.timeout = 10  # 默认超时时间
        self.poll_frequency = 0.5  # 默认轮询频率
        
        # 如果提供了URL，则导航到该页面
        if url:
            self.open(url)
    
    def open(self, url: str) -> None:
        """
        打开页面
        
        Args:
            url: 页面URL
        """
        logger.info(f"导航到页面: {url}")
        self.driver.get(url)
    
    def find_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """
        查找单个元素
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            WebElement实例
            
        Raises:
            TimeoutException: 如果在指定时间内未找到元素
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"找不到元素: {locator}")
            raise
    
    def find_elements(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[WebElement]:
        """
        查找多个元素
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            WebElement列表
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.warning(f"找不到元素: {locator}")
            return []
    
    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """
        等待元素可见
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            WebElement实例
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"元素未变为可见: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """
        等待元素可点击
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            WebElement实例
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            logger.error(f"元素未变为可点击: {locator}")
            raise
    
    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        点击元素
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
        """
        element = self.wait_for_element_clickable(locator, timeout)
        try:
            element.click()
            logger.debug(f"点击元素: {locator}")
        except Exception as e:
            logger.error(f"点击元素失败: {locator}, 错误: {e}")
            # 尝试使用JavaScript点击
            self.js_click(element)
    
    def js_click(self, element: Union[WebElement, Tuple[By, str]]) -> None:
        """
        使用JavaScript点击元素
        
        Args:
            element: WebElement实例或元素定位器
        """
        if not isinstance(element, WebElement):
            element = self.find_element(element)
            
        try:
            self.driver.execute_script("arguments[0].click();", element)
            logger.debug("使用JavaScript点击元素")
        except Exception as e:
            logger.error(f"JavaScript点击失败: {e}")
            raise
    
    def input_text(self, locator: Tuple[By, str], text: str, clear: bool = True, timeout: Optional[int] = None) -> None:
        """
        向输入框输入文本
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            text: 要输入的文本
            clear: 输入前是否清除现有文本
            timeout: 超时时间，如不指定则使用默认值
        """
        element = self.wait_for_element_visible(locator, timeout)
        
        if clear:
            element.clear()
            
        element.send_keys(text)
        logger.debug(f"输入文本 '{text}' 到元素: {locator}")
    
    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        获取元素文本
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            元素文本
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def get_attribute(self, locator: Tuple[By, str], attribute: str, timeout: Optional[int] = None) -> str:
        """
        获取元素属性
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            attribute: 属性名
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            属性值
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = 1) -> bool:
        """
        检查元素是否存在
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间
            
        Returns:
            如果元素存在返回True，否则返回False
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def hover(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        鼠标悬停在元素上
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
        """
        element = self.wait_for_element_visible(locator, timeout)
        
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        logger.debug(f"鼠标悬停在元素上: {locator}")
    
    def scroll_to_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        滚动到元素位置
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
        """
        element = self.find_element(locator, timeout)
        
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        logger.debug(f"滚动到元素: {locator}")
        time.sleep(0.5)  # 等待滚动完成
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间，如不指定则使用默认值
        """
        timeout = timeout or self.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.debug("页面加载完成")
        except TimeoutException:
            logger.warning("页面加载超时")
    
    def refresh_page(self) -> None:
        """刷新当前页面"""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.debug("页面已刷新")
    
    def go_back(self) -> None:
        """返回上一页"""
        self.driver.back()
        self.wait_for_page_load()
        logger.debug("返回上一页")
    
    def go_forward(self) -> None:
        """前进到下一页"""
        self.driver.forward()
        self.wait_for_page_load()
        logger.debug("前进到下一页")
    
    def switch_to_frame(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        切换到iframe
        
        Args:
            locator: frame元素定位器，格式为(By.XXX, 'value')
            timeout: 超时时间，如不指定则使用默认值
        """
        timeout = timeout or self.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
            logger.debug(f"切换到iframe: {locator}")
        except TimeoutException:
            logger.error(f"无法切换到iframe: {locator}")
            raise
    
    def switch_to_default_content(self) -> None:
        """切换回主文档"""
        self.driver.switch_to.default_content()
        logger.debug("切换回主文档")
    
    def get_page_title(self) -> str:
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.driver.title
    
    def get_page_url(self) -> str:
        """
        获取当前页面URL
        
        Returns:
            当前页面URL
        """
        return self.driver.current_url
    
    def take_screenshot(self, filename: str) -> str:
        """
        截取当前页面截图
        
        Args:
            filename: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not filename.endswith(".png"):
            filename += ".png"
            
        filepath = f"screenshots/{filename}"
        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            raise
    
    def execute_script(self, script: str, *args) -> any:
        """
        执行JavaScript脚本
        
        Args:
            script: JavaScript脚本
            *args: 脚本参数
            
        Returns:
            脚本执行结果
        """
        return self.driver.execute_script(script, *args)
    
    def wait_for(self, condition: Callable[[WebDriver], Any], timeout: Optional[int] = None, 
                 message: str = "") -> Any:
        """
        通用等待方法，可以等待任何自定义条件
        
        Args:
            condition: 等待条件，一个接受WebDriver参数并返回布尔值的函数
            timeout: 超时时间，如不指定则使用默认值
            message: 超时时的错误消息
            
        Returns:
            condition函数的返回值
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                condition, message
            )
        except TimeoutException:
            logger.error(f"等待条件超时: {message or '未指定条件'}")
            raise
    
    def wait_for_text_present(self, locator: Tuple[By, str], text: str, 
                            timeout: Optional[int] = None) -> WebElement:
        """
        等待元素中出现指定文本
        
        Args:
            locator: 元素定位器，格式为(By.XXX, 'value')
            text: 要等待的文本
            timeout: 超时时间，如不指定则使用默认值
            
        Returns:
            包含文本的WebElement实例
        """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout, self.poll_frequency).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            logger.error(f"元素中未出现文本 '{text}': {locator}")
            raise 