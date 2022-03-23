# -*- coding: utf-8 -*-
# @Time    : 2022/3/18
# @Author  : 阿宋
# @File    : test_01_7_add_coupon.py

from base.browser_driver import cache_chrome_driver
from page.coupon_list import CouponList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestAddCoupon(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.cl = CouponList(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # @data(["sun", "qdwx@2021"])
    # @unpack
    # def test_01_login(self, account, password):
    #     status = self.lg.login(account, password)
    #     self.assertTrue(status, "登陆成功了")

    @file_data("../test_data/add_coupon_must.yaml")
    def test_02_add_coupon_must(self, **kwargs):
        status = self.cl.add_coupon_must(kwargs["send_ac"], kwargs["use_ac"], kwargs["builds_num"])
        self.assertTrue(status, "生成优惠券失败啦")


if __name__ == '__main__':
    unittest.main()
