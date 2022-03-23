# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : test_01_10_business_coupon.py
from unittest import skip

from base.browser_driver import cache_chrome_driver
from page.coupon_business_list import CouponBusinessList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data


@ddt
class TestCouponBusiness(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.cbl = CouponBusinessList(cls.driver)

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
    @file_data("../test_data/add_business_data.yaml")
    def test_02_add_business(self, **kwargs):
        status = self.cbl.add_business(kwargs['ac_name'], kwargs['business_name'])
        self.assertTrue(status, "优惠券业务管理添加失败")

    # @skip
    @data("test")
    def test_03_fix_business(self, business_name):
        status = self.cbl.edit_business(business_name)
        self.assertTrue(status, "优惠券业务管理编辑失败")

    def test_04_del_business(self):
        status = self.cbl.delete_business()
        self.assertTrue(status, "优惠券业务管理删除失败")


if __name__ == '__main__':
    unittest.main()
