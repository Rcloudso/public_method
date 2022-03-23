# -*- coding: UTF-8 -*-
from base.keys import KeyWeb
from base.browser_driver import chrome_driver
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class Login(KeyWeb):
    login_url = base_url + "user/login?redirect=%2F"
    account_input = ("id", "username")
    password_input = ("id", "password")
    code_input = ("id", "inputCode")
    login_button = ("xpath", "//button[@type='submit']")

    def login(self, account=None, password=None):
        self.open_url(self.login_url)
        log.info("已打开登录网址{}".format(self.login_url))

        self.input_(*self.account_input, account)
        log.info("已输入账号：{}".format(account))

        self.input_(*self.password_input, password)
        log.info("已输入密码：{}".format(password))

        self.ele_sleep(5)

        log.info("请输入图形验证码，您将有5秒钟的时间来完成")

        self.click_element(*self.login_button)
        log.info("已点击登录按钮")

        self.ele_sleep(3)

        if self.loctor(*self.login_button) is False:
            log.info("登陆成功咯！")
            return True
        else:
            log.error("登陆失败了，请检查输入的账号密码和验证码是否正确！")
            return False
