# -*- coding: utf-8 -*-
# @Time    : 2022/3/19
# @Author  : 阿宋
# @File    : test_01_5_edit_base_coupon.py
from unittest import skip

from base.browser_driver import cache_chrome_driver
from page.base_coupon_list import BaseCouponList
from page.login_page import Login
import unittest
from ddt import ddt, data, unpack


@ddt
class TestAddCoupon(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = cache_chrome_driver()
        self.lg = Login(self.driver)
        self.bcl = BaseCouponList(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()

    @data("1122")
    def test_01_edit_base_must(self, coupon_name):
        status = self.bcl.edit_base_coupon_must(coupon_name)
        self.assertTrue(status, "编辑失败啦")
        self.bcl.del_base_coupon()

    @skip
    @data(["11223", "备注备注备注"])
    @unpack
    def test_02_edit_base_all(self, coupon_name, remake):
        status = self.bcl.edit_base_coupon_all(coupon_name, remake)
        self.assertTrue(status, "编辑失败啦")
        self.bcl.del_base_coupon()


if __name__ == '__main__':
    unittest.main()
