# -*- coding: utf-8 -*-
# @Time    : 2022/3/19
# @Author  : 阿宋
# @File    : test_01_8_del_coupon.py

from base.browser_driver import cache_chrome_driver
from page.coupon_list import CouponList
from page.login_page import Login
import unittest
from ddt import ddt, data


@ddt
class TestDelCoupon(unittest.TestCase):
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

    @data("小宋")
    def test_02_del_coupon(self, ac_name):
        status = self.cl.del_cp_coupon(ac_name)
        self.assertTrue(status, "作废优惠券失败")


if __name__ == '__main__':
    unittest.main()
