# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : test_01_9_fix_cp_goods.py
from unittest import skip

from base.browser_driver import cache_chrome_driver
from page.coupon_batch_list import CouponBatchList
from page.login_page import Login
import unittest
from ddt import ddt, data


@ddt
class TestCouponBatch(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = cache_chrome_driver()
        self.lg = Login(self.driver)
        self.cbl = CouponBatchList(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()

    # 调试用
    # @data(["sun", "qdwx@2021"])
    # @unpack
    # def test_01_login(self, account, password):
    #     status = self.lg.login(account, password)
    #     self.assertTrue(status, "登陆成功了")

    # @skip
    @data("小宋")
    def test_02_fix_coupon_goods(self, ac_name):
        status = self.cbl.fix_cp_goods(ac_name)
        self.assertTrue(status, "优惠券批次商品更改失败")

    # @skip
    @data("小宋")
    def test_03_fix_coupon_time(self, ac_name):
        status = self.cbl.fix_time(ac_name)
        self.assertTrue(status, "优惠券批次有效期更改失败")

    @data("小宋")
    def test_04_del_batch_coupon(self, ac_name):
        status = self.cbl.delete_batch_cp(ac_name)
        self.assertTrue(status, "优惠券批次作废失败")


if __name__ == '__main__':
    unittest.main()
