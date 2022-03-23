# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : exchange_code_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class ExchangeCodeList(KeyWeb):
    coupon_batch_url = base_url + "exchange/ExchangeNameList"

    # 新增按钮
    add_button = ("xpath", "//span[text()='新 增']/..")

    # 兑换码类型选择
    exchange_type = ("xpath", "//div[@id='exchangeCouponType']/div/div")
    first_type = ("xpath", "//*[@id='test-uuid']/ul/li[2]")
    # 兑换码名称
    exchange_name = ("id", "couponName")
    # 兑换码金额
    exchange_price = ("id", "couponPrice")
    # 备注
    remake = ("id", "couponDisp")
    add_sure = ("xpath", "//span[text()='确 定']/..")

    # 提示语文本
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")

    def assert_result(self):
        self.ele_sleep(1)
        result = self.get_text(*self.toast)
        if "成功" in result:
            log.info("=====业务流程成功结束咯=====")
            return True
        else:
            log.error(result)
            log.info("=====业务流程失败结束咯=====")
            return False

    def add_exchange_code(self, exchange_name, exchange_price):
        self.open_url(self.coupon_batch_url)
        log.info("已打开兑换码管理页面，url为: %s" % self.coupon_batch_url)
        self.click_element(*self.add_button)
        log.info("点击 %s 按钮" % self.get_text(*self.add_button))
        self.click_element(*self.exchange_type)
        log.info("点击兑换码类型选择框")
        self.ele_sleep(2)
        log.info("选择 %s 类型" % self.get_text(*self.first_type))
        self.click_element(*self.first_type)
        log.info("选择 %s 类型" % self.get_text(*self.first_type))
        self.input_(*self.exchange_name, exchange_name)
        log.info("输入兑换码名称: %s " % exchange_name)
        self.mouse_input(*self.exchange_price, exchange_price)
        log.info("已输入标签优先级: {}".format(exchange_price))
        self.click_element(*self.add_sure)
        log.info("点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()
