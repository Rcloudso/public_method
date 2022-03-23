# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : test_01_12_exchange_list.py


from unittest import skip

from base.browser_driver import cache_chrome_driver
from page.exchange_code_list import ExchangeCodeList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data


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
    # @data(["sun", "qdwx@2021"])
    # @unpack
    # def test_01_login(self, account, password):
    #     status = self.lg.login(account, password)
    #     self.assertTrue(status, "登陆成功了")

    # @skip
    @file_data("../test_data/add_exchange_data.yaml")
    def test_02_add_label(self, **kwargs):
        status = self.ecl.add_exchange_code(kwargs['exchange_name'], kwargs['exchange_price'])
        self.assertTrue(status, "兑换码添加失败")

    # @skip
    # @file_data("../test_data/edit_label_data.yaml")
    # def test_03_edit_label(self, **kwargs):
    #     status = self.cll.edit_label(kwargs['label_name'], kwargs['label_priority'],
    #                                  kwargs['label_logic'])
    #     self.assertTrue(status, "优惠券业务管理编辑失败")
    #
    # def test_04_delete_label(self):
    #     status = self.cll.delete_label()
    #     self.assertTrue(status, "优惠券业务管理删除失败")


if __name__ == '__main__':
    unittest.main()
