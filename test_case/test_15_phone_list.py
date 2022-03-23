# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : test_15_phone_list.py

from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.phone_list import PhoneList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestExchange(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.pl = PhoneList(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # 调试用
    @skipIf(AttributeError, "已登录，无需登录")
    @data(["sun", "qdwx@2021"])
    @unpack
    def test_01_login(self, account, password):
        status = self.lg.login(account, password)
        self.assertTrue(status, "登陆失败了")

    # @skip
    @data("1516660")
    def test_02_add_phone(self, phone_num):
        status = self.pl.add_phone(phone_num)
        self.assertTrue(status, "添加手机号归属地失败啦")

    # @skip
    @data(["1516660", "1516661", "临沂"])
    @unpack
    def test_03_edit_phone(self, phone_number, phone_num, city_name):
        status = self.pl.edit_phone(phone_number, phone_num, city_name)
        self.assertTrue(status, "编辑手机号归属地失败啦")

    # @skip
    @data("1516660")
    def test_04_del_phone(self, phone_number):
        status = self.pl.del_phone(phone_number)
        self.assertTrue(status, "删除手机号归属地失败啦")


if __name__ == '__main__':
    unittest.main()
