# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : test_14_exchange_batch_list.py

from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.exchange_code_batch_list import ExchangeBatchList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestExchange(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.ebl = ExchangeBatchList(cls.driver)

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
    @data("宋")
    def test_02_edit_goods(self, ac_name):
        status = self.ebl.edit_batch_goods(ac_name)
        self.assertTrue(status, "兑换码批次修改商品失败了")

    # @skip
    @data("宋")
    def test_03_edit_time(self, ac_name):
        status = self.ebl.fix_time(ac_name)
        self.assertTrue(status, "兑换码批次修改有效期失败了")

    @data("宋")
    def test_04_del_exchange(self, ac_name):
        status = self.ebl.delete_batch_exchange(ac_name)
        self.assertTrue(status, "兑换码批次修改有效期失败了")


if __name__ == '__main__':
    unittest.main()
