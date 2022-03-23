# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : test_12_base_exchange_list.py


from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.exchange_base_code_list import BaseExchangeCodeList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestBaseExchange(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.ecl = BaseExchangeCodeList(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # 调试用
    @skipIf(AttributeError, "已登录，无需登录")
    @data(["sun", "qdwx@2021"])
    @unpack
    def test_01_login(self, account, password):
        status = self.lg.login(account, password)
        self.assertTrue(status, "登陆成功了")

    # @skip
    @file_data("../test_data/add_exchange_data.yaml")
    def test_02_add_base_exchange(self, **kwargs):
        status = self.ecl.add_exchange_code(kwargs['exchange_name'], kwargs['exchange_price'])
        self.assertTrue(status, "基础兑换码添加失败")


if __name__ == '__main__':
    unittest.main()
