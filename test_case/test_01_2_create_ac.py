# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:test_01_2_create_ac
# DateTime:2022/3/17


from base.browser_driver import cache_chrome_driver
from page.login_page import Login
from page.create_activity import CreateActivity
from page.add_goods import AddGoods
from ddt import ddt, data, unpack, file_data
import unittest


@ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.ca = CreateActivity(cls.driver)
        cls.ag = AddGoods(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # @data(["sun", "qdwx@2021"])
    # @unpack
    # def test_01_login(self, account, password):
    #     status = self.lg.login(account, password)
    #     self.assertTrue(status, "登陆成功了")

    @file_data("../test_data/create_activity.yaml")
    def test_02_create_ac(self, **kwargs):
        status = self.ca.create_activity_must(kwargs["ac_name"], kwargs["ac_title"])
        self.assertTrue(status, "创建失败啦")

    @file_data("../test_data/create_all_activity.yaml")
    def test_03_create_ac_all(self, **kwargs):
        status = self.ca.create_activity_all(kwargs["ac_name"], kwargs["ac_title"], kwargs["remake_text"])
        self.assertTrue(status, "创建失败啦")

    @file_data("../test_data/create_goods.yaml")
    def test_04_create_goods(self, **kwargs):
        status = self.ag.create_goods(kwargs["contract_price"], kwargs["cash_price"], kwargs["points_price"],
                                      kwargs["all_input_num"])
        self.assertTrue(status, "创建失败啦")

    @file_data("../test_data/create_all_goods.yaml")
    def test_05_create_goods_all(self, **kwargs):
        status = self.ag.create_all_goods(kwargs["contract_price"], kwargs["cash_price"], kwargs["points_price"],
                                          kwargs["all_input_num"], kwargs["recommend"], kwargs["remake"],
                                          kwargs["goods_info"])
        self.assertTrue(status, "创建失败啦")


if __name__ == '__main__':
    unittest.main()
