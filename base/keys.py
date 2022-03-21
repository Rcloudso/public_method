"""
    底层工具类
    log函数做调试用
"""

from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from My_option.Log_color import HandleLog

log = HandleLog()


class KeyWeb:

    # 构造函数，初始化使用，implicitly_wait为全局隐式等待时长，里面的数字可以随意更改
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(8)

    # 访问网址，传参为url
    def open_url(self, url):
        self.driver.get(url)

    # 刷新网页
    def refresh(self):
        self.driver.refresh()

    # 后退界面
    def back(self):
        self.driver.back()

    # 前进界面
    def forward(self):
        self.driver.forward()

    # 元素定位，name是定位方法，value是定位元素的值
    def loctor(self, name, value):
        try:
            return self.driver.find_element(name, value)
        except NoSuchElementException:
            return False

    # 返回元素列表，暂时没用到，还要研究下
    def loctors(self, name, value):
        try:
            return self.driver.find_elements(name, value)
        except NoSuchElementException:
            return False

    # 元素点击，点击定位到的元素
    def click_element(self, name, value):
        self.loctor(name, value).click()

    # 切换iframe，iframe有id时，直接传值即可；否则就是传入iframe的定位方法和定位的值
    def switch_frame(self, value, name=None):
        if name is None:
            self.driver.switch_to.frame(value)

        else:
            self.driver.switch_to.frame(self.loctor(name, value))

    # 输入内容，在定位到的元素中输入内容（为了防止输入框中有默认的内容，所以使用了一次clear()方法来清除输入框的内容）
    def input_(self, name, value, text):
        ele = self.loctor(name, value)
        # ele.clear()
        ele.send_keys(text)

    def clear_input(self, name, value, text):
        ele = self.loctor(name, value)
        ele.clear()
        ele.send_keys(text)

    # 切换默认界面，每次切换iframe都要切换回来；切换句柄时视情况而定
    def default(self):
        self.driver.switch_to.default_content()

    # 强制等待，参数为要等待的时间
    def ele_sleep(self, text):
        sleep(int(text))

    # 显示等待
    def ele_wait(self, name, value, text):
        """
        等待指定的元素加载出来，超时会报timeout
        :param name: 元素定位方法
        :param value: 元素定位的值
        :param text: 等待该元素加载的最大等待时间
        :return:
        """
        return WebDriverWait(self.driver, text, 0.5).until(
            lambda el: self.loctor(name, value), message='元素查找失败')

    # 退出，退出浏览器驱动
    def quit(self):
        self.driver.quit()

    # 获取元素文本信息
    def get_text(self, name, value):
        """
        :param name: 元素定位方法
        :param value: 元素定位值
        :return:
        """
        return self.loctor(name, value).text

    # 获取元素属性信息
    def get_attribute(self, name, value, text):
        """
        :param name: 元素定位方法
        :param value: 元素定位值
        :param text: 元素属性的key
        :return:
        """
        return self.loctor(name, value).get_attribute(text)

    # 断言文本信息
    def assert_text(self, name, value, expected):
        """
        通过元素文本与预期值进行断言，断言通过返回True，断言失败返回False
        :param name: 元素定位方法
        :param value: 元素定位的值
        :param expected: 预期值
        :return:
        """
        try:
            reality = self.get_text(name, value)
            assert expected == reality, "断言失败！{0}!={1}".format(expected, reality)
            return True
        except AssertionError:
            return False

    # 断言属性信息
    def assert_attr(self, name, value, text, expected):
        """
        通过元素m某个属性值与预期值进行断言，断言通过返回True，断言失败返回False
        :param name: 元素定位方法
        :param value: 元素定位值
        :param text: 元素属性的key
        :param expected: 预期值
        :return:
        """
        try:
            reality = self.loctor(name, value).get_attribute(text)
            assert expected == reality, "断言失败！{0}!={1}".format(expected, reality)
            return True
        except AssertionError:
            return False

    # 切换句柄
    def handles_switch(self, close=False, index=1):
        """
        切换窗口句柄，首先获取当前浏览器所有句柄（返回一个列表），如果close为True，就关闭当前页面；默认为False，不关闭当前页。
        Index为句柄的索引号，因为获取句柄返回的是列表，索引从0开始，-1表示倒数第一个
        :param close:
        :param index:
        :return:
        """
        handles = self.driver.window_handles
        if close:
            self.close_page()
        self.driver.switch_to.window(handles[index])

    # 关闭页面，关闭当前页
    def close_page(self):
        self.driver.close()

    # JS执行器中的点击
    def js_click(self, name, value):
        """
        调用JS执行器进行点击操作，成功操作返回True，操作失败返回False，并且有log生成
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        try:
            ele = self.loctor(name, value)
            self.driver.execute_script("arguments[0].click();", ele)
            return True
        except Exception as e:
            log.error(e)
            return False

    # JS执行器中的滑动至指定元素
    def js_scroll(self, name, value):
        """
        调用JS执行器进行滑动至目标元素操作，成功操作返回True，操作失败返回False，并且有log生成
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        try:
            js = "arguments[0].scrollIntoView();"
            self.driver.execute_script(js, self.loctor(name, value))
            return True
        except Exception as e:
            log.error(e)
            return False

    # JS执行器中的删除元素属性
    def js_remove(self, text, name, value):
        """
        调用JS执行器进行删除元素属性操作，成功操作返回True，操作失败返回False，并且有log生成
        :param text: 元素属性的key
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        try:
            js = "arguments[0].removeAttribute(arguments[1]);"
            self.driver.execute_script(js, self.loctor(name, value), text)
            return True
        except Exception as e:
            log.error(e)
            return False

    # JS执行器中的设置元素属性
    def js_set(self, name, value, att_name, att_value):
        """
        调用JS执行器进行设置元素属性操作，成功操作返回True，操作失败返回False，并且有log生成
        :param name: 元素定位方法
        :param value: 元素定位的值
        :param att_name: 被修改属性的key
        :param att_value: 将被修改属性的值改为xxx
        :return:
        """
        try:
            js = "arguments[0].setAttribute(arguments[1], arguments[2]);"
            self.driver.execute_script(js, self.loctor(name, value), att_name, att_value)
            return True
        except Exception as e:
            log.error(e)
            return False

    # JS执行器中的获取元素全部内容（包括标签名）
    def js_html(self, name, value):
        """
        调用JS执行器进行获取元素的全部内容，包含标签名，成功操作返回True，操作失败返回False，并且有log生成
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        try:
            js = "return arguments[0].innerHTML"
            return self.driver.execute_script(js, self.loctor(name, value))
        except Exception as e:
            log.error(e)
            return False

    # JS执行器中的获取文本内容
    def js_text(self, name, value):
        """
        调用JS执行器进行获取元素的文本，成功操作返回True，操作失败返回False，并且有log生成
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        try:
            js = "return arguments[0].innerTEXT"
            return self.driver.execute_script(js, self.loctor(name, value))
        except Exception as e:
            log.error(e)
            return False

    # 鼠标滑动至元素处
    def move_ele(self, name, value):
        """
        将鼠标滑动至目标元素处
        :param name: 元素定位方法
        :param value: 元素定位的值
        :return:
        """
        ActionChains(self.driver).move_to_element(self.loctor(name, value)).perform()
        return self

    def mouse_input(self, name, value, text):
        ActionChains(self.driver).send_keys_to_element(self.loctor(name, value), text).perform()
        return self

    def move_ele_click(self, name, value, xoffset, yoffset):
        """
        将鼠标滑动至目标元素处
        :param name: 元素定位方法
        :param value: 元素定位的值
        :param xoffset: 元素的x坐标
        :param yoffset: 元素的y坐标
        :return:
        """
        ActionChains(self.driver).move_to_element(self.loctor(name, value)).move_by_offset(xoffset,
                                                                                           yoffset).click().perform()
        return self

    def mouse_click(self, name, value):
        ActionChains(self.driver).click(on_element=self.loctor(name, value)).perform()
        return self

    def mouse_double_click(self, name, value):
        ActionChains(self.driver).double_click(on_element=self.loctor(name, value)).perform()
        return self

    def mouse_clear_input(self, name, value, text):
        ActionChains(self.driver).key_down(Keys.CONTROL, self.loctor(name, value)).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
        return self

    def get_location(self, name, value, coordinate):
        if self.loctor(name, value):
            if coordinate == "x" or "y":
                return self.loctor(name, value).location.get(coordinate)
            else:
                raise Exception("请输入坐标轴'x'或者'y'！")
        return False

    # select方法封装,元素必须要有select标签
    def select_(self, name, value):
        return Select(self.loctor(name, value))

    # 通过value值查找select标签
    def select_value(self, name, value, text):
        select = self.select_(name, value)
        select.deselect_all()
        select.select_by_value(text)

    # 通过text文本查找select标签
    def select_text(self, name, value, text):
        select = self.select_(name, value)
        select.deselect_all()
        select.select_by_visible_text(text)

    # 通过index索引值查找select标签
    def select_index(self, name, value, text):
        select = self.select_(name, value)
        select.deselect_all()
        select.select_by_index(text)

    # alert弹窗信息
    def alert_message(self):
        alert = self.driver.switch_to.alert
        return alert.text

    # # alert弹窗处理,没想好怎么处理这三种弹窗
    # def alert_accept_or_dismiss(self):
    #     alert = self.driver.switch_to.alert
    #     alert.accept()
    #     alert.dismiss()
    #     alert.send_keys()
