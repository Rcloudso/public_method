# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : test_01_11_label_list.py

from unittest import skip

from base.browser_driver import cache_chrome_driver
from page.coupon_label_list import CouponLabelList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data


@ddt
class TestCouponLable(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.cll = CouponLabelList(cls.driver)

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
    @file_data("../test_data/add_label_data.yaml")
    def test_02_add_label(self, **kwargs):
        status = self.cll.add_label(kwargs['ac_name'], kwargs['label_name'], kwargs['label_priority'],
                                    kwargs['label_logic'])
        self.assertTrue(status, "优惠券用户标签添加失败")

    # @skip
    @file_data("../test_data/edit_label_data.yaml")
    def test_03_edit_label(self, **kwargs):
        status = self.cll.edit_label(kwargs['label_name'], kwargs['label_priority'],
                                     kwargs['label_logic'])
        self.assertTrue(status, "优惠券业务管理编辑失败")

    def test_04_delete_label(self):
        status = self.cll.delete_label()
        self.assertTrue(status, "优惠券业务管理删除失败")


if __name__ == '__main__':
    unittest.main()
