# -*- coding: utf-8 -*-
# @Time    : 2022/3/19
# @Author  : 阿宋
# @File    : test_01_6_delete_base_coupon.py
from unittest import skipIf

from ddt import data, unpack

from base.browser_driver import cache_chrome_driver
from page.base_coupon_list import BaseCouponList
from page.login_page import Login
import unittest


class TestDeleteBase(unittest.TestCase):
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

    def test_02_delete_used_base_coupon(self):
        self.bcl.del_base_coupon()
        status = self.bcl.assert_result()
        self.assertFalse(status, "删除已生成批次的优惠券成功了,请排查问题")


if __name__ == '__main__':
    unittest.main()
