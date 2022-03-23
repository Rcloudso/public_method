# -*- coding: utf-8 -*-
# @Time    : 2022/3/18
# @Author  : 阿宋
# @File    : test_01_4_add_base_coupon.py
from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.base_coupon_list import BaseCouponList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestAddBase(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = cache_chrome_driver()
        self.lg = Login(self.driver)
        self.bcl = BaseCouponList(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()

    # 调试用
    @skipIf(AttributeError, "已登录，无需登录")
    @data(["sun", "qdwx@2021"])
    @unpack
    def test_01_login(self, account, password):
        status = self.lg.login(account, password)
        self.assertTrue(status, "登陆成功了")

    # @skip
    @file_data("../test_data/add_base_coupon_must.yaml")
    def test_02_add_base_must(self, **kwargs):
        status = self.bcl.add_base_coupon_must(kwargs["coupon_name"], kwargs["coupon_price"], kwargs["lowest_price"])
        self.assertTrue(status, "添加基础优惠券失败啦")

    # @skip
    @file_data("../test_data/add_base_coupon_all.yaml")
    def test_03_add_base_all(self, **kwargs):
        status = self.bcl.add_base_coupon_all(kwargs["coupon_name"], kwargs["coupon_price"], kwargs["lowest_price"],
                                              kwargs["remake"])
        self.assertTrue(status, "添加基础优惠券失败啦")


if __name__ == '__main__':
    unittest.main()
