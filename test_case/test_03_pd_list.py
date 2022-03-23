# -*- coding: utf-8 -*-
# @Time    : 2022/3/18
# @Author  : 阿宋
# @File    : test_01_3_pd_list.py
from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.product_list import ProductList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestAddProduct(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = cache_chrome_driver()
        self.lg = Login(self.driver)
        self.ap = ProductList(self.driver)

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
    @file_data("../test_data/add_product.yaml")
    def test_02_add_product(self, **kwargs):
        status = self.ap.add_product_must(kwargs["product_id"], kwargs["product_name"], kwargs["offical_price"])
        self.assertTrue(status, "添加产品失败啦")

    # @skip
    @file_data("../test_data/add_all_product.yaml")
    def test_03_add_all_product(self, **kwargs):
        status = self.ap.add_product_all(kwargs["product_id"], kwargs["product_name"], kwargs["offical_price"],
                                         kwargs["stock_num"], kwargs["need_now"], kwargs["telephone"],
                                         kwargs["account_msg"], kwargs["brand"], kwargs["store_url"])
        self.assertTrue(status, "添加产品失败啦")

    # @skip
    def test_04_up_down_product(self):
        status = self.ap.updown_product()
        if status:
            up_status = self.ap.updown_product()
            self.assertTrue(up_status, "上架失败啦")
        else:
            raise Exception("下架失败啦")


if __name__ == '__main__':
    unittest.main()
