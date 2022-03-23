# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : test_16_user_level_list.py

from unittest import skip, skipIf

from base.browser_driver import cache_chrome_driver
from page.user_level_list import UserLevelList
from page.login_page import Login
import unittest
from ddt import ddt, file_data, data, unpack


@ddt
class TestExchange(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = cache_chrome_driver()
        cls.lg = Login(cls.driver)
        cls.ull = UserLevelList(cls.driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    # 调试用
    @skipIf(AttributeError, "已登录，无需登录")
    @data(["sun", "qdwx@2021"])
    @unpack
    def test_01_login(self, account, password):
        status = self.lg.login(account, password)
        self.assertTrue(status, "登陆失败了")

    # @skip
    @data("宋")
    def test_02_add_user_level(self, ac_name):
        status = self.ull.add_user_level_must(ac_name)
        self.assertTrue(status, "新增用户等级(必填)失败啦")

    # @skip
    @file_data("../test_data/add_user_level_all.yaml")
    def test_03_add_user_level_all(self, **kwargs):
        status = self.ull.add_user_level_all(kwargs['ac_name'], kwargs['level'], kwargs['phone'], kwargs['phone_md5'],
                                             kwargs['card_id'], kwargs['card_id_md5'], kwargs['remake'])
        self.assertTrue(status, "新增用户等级(全填)失败啦")

    # @skip
    @file_data("../test_data/edit_user_level_all.yaml")
    def test_04_edit_user_level_all(self, **kwargs):
        status = self.ull.edit_user_level(kwargs['ac_name'], kwargs['level'], kwargs['phone'], kwargs['phone_md5'],
                                          kwargs['card_id'], kwargs['card_id_md5'], kwargs['remake'])
        self.assertTrue(status, "编辑用户等级失败啦")

    @data("王炳文")
    def test_05_delete_user_level(self, ac_name):
        status = self.ull.delete_user_level(ac_name)
        self.assertTrue(status, "删除用户等级失败啦")


if __name__ == '__main__':
    unittest.main()
