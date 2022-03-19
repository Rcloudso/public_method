# -*- coding: utf-8 -*-
# @Time    : 2022/3/19
# @Author  : 阿宋
# @File    : test_01_8_del_coupon.py

from base.browser_driver import cache_chrome_driver
from page.coupon_list import CouponList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestAddProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.cl = CouponList(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # 调试用
    # @data(["sun", "qdwx@2021"])
    # @unpack
    # def test_01_login(self, account, password):
    #     status = self.lg.login(account, password)
    #     self.assertTrue(status, "登陆成功了")

    def test_02_del_coupon(self):
        self.cl.search_ac_cp("小宋")
        self.cl.ele_sleep(3)


if __name__ == '__main__':
    unittest.main()
