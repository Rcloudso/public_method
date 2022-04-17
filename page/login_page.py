# -*- coding: UTF-8 -*-
import os
from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog
from Conf.A_common import cover_img, read_code

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
        cover_path = self.save_img("test.png")
        read_path = cover_img(cover_path, "test1.png")
        code = read_code(read_path)

        self.input_(*self.account_input, account)
        log.info("已输入账号：{}".format(account))

        self.input_(*self.password_input, password)
        log.info("已输入密码：{}".format(password))

        self.input_(*self.code_input, code)
        log.info("已输入验证码:{}".format(code))

        self.click_element(*self.login_button)
        log.info("已点击登录按钮")

        self.ele_sleep(3)

        if self.loctor(*self.login_button) is False:
            log.info("登陆成功咯！")
            return True
        else:
            log.error("登陆失败了，请检查输入的账号密码和验证码是否正确！")
            return False

# if __name__ == '__main__':
