# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:test_01_1_login
# DateTime:2022/3/17

from base.browser_driver import chrome_driver
from page.login_page import Login

from ddt import ddt, file_data
import unittest


@ddt
class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = chrome_driver()
        self.lg = Login(self.driver)

    def tearDown(self) -> None:
        self.driver.quit()

    @file_data("../test_data/login.yaml")
    def test_login(self, **kwargs):
        status = self.lg.login(kwargs["account"], kwargs["password"])
        self.assertTrue(status, "登陆失败了")


if __name__ == '__main__':
    unittest.main()
