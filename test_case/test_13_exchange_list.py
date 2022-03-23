# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : test_13_exchange_list.py

from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.exchange_code_list import ExchangeCodeList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestExchange(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.ecl = ExchangeCodeList(cls.driver)

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
    @file_data("../test_data/create_exchange_data.yaml")
    def test_02_add_exchange(self, **kwargs):
        status = self.ecl.create_exchange_code(kwargs['exchange_name'], kwargs['send_ac'], kwargs['use_ac'],
                                               kwargs['builds_num'])
        self.assertTrue(status, "生成兑换码失败")

    @data("宋")
    def test_03_edit_exchange_time(self, ac_name):
        status = self.ecl.edit_exchange_code_time(ac_name)
        self.assertTrue(status, "修改兑换码有效期失败")


if __name__ == '__main__':
    unittest.main()
