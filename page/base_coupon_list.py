# -*- coding: utf-8 -*-
# @Time    : 2022/3/18
# @Author  : 阿宋
# @File    : base_coupon_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class BaseCouponList(KeyWeb):
    base_coupon_url = base_url + "coupons/CouponNameList"
    # 新增基础优惠券按钮
    add_base_coupon_button = ("xpath", "//span[text()='新 增']/..")
    # 编辑首个基础优惠券
    edit_base_coupon_button = ("xpath", "//a[text()='编辑']")
    # 删除按钮
    del_base_coupon_button = ("xpath", "//a[text()='删除']")
    # 优惠券类型选择
    coupon_type = ("xpath", "//div[@id='couponType']/div")
    # 优惠券类型选择列表
    coupon_type_list = ("xpath", "//ul[@role='listbox']/li")
    # 选择第一个优惠券类型
    first_coupon_type = ("xpath", "//li[@role='option' and contains(text(), '直接')]")
    # 优惠券名称输入
    coupon_name = ("xpath", "(//input[@placeholder='请输入优惠券名称'])[2]")
    # 优惠券金额输入
    coupon_price = ("xpath", "//input[contains(@placeholder, '优惠券金额')]")
    # 最低消费金额输入
    lowest_price = ("xpath", "//input[contains(@placeholder, '最低消费')]")
    # 备注输入
    remake = ("xpath", "//input[contains(@placeholder, '备注')]")
    # 添加确定
    add_sure = ("xpath", "//span[contains(text(), '确')]/..")
    # 二级确认
    second_sure = ("xpath", "(//span[contains(text(), '确')]/..)[2]")
    # 提示语
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")
    # 确定后，每一栏报错时显示的信息
    error_msg = ("xpath", "//div[@class='ant-form-explain']")

    def choose_coupon_type(self):
        self.ele_sleep(1)
        self.click_element(*self.coupon_type)
        log.info("已点击优惠券类型选择")
        self.ele_wait(*self.first_coupon_type, 10)
        self.click_element(*self.first_coupon_type)
        log.info("已选择第一种优惠券类型")
        # ToDo: 尝试获取元素列表，通过输入数值来选择
        # coupon_type_lists = self.loctors(*self.coupon_type_list)
        # for coupon_type_list in coupon_type_lists:
        #     self.driver.find_element()
        #     txt = coupon_type_list.text
        #     print(txt)

    def base_coupon_must(self, coupon_name, coupon_price, lowest_price):
        self.open_url(self.base_coupon_url)
        log.info("已打开优惠券管理页面，url为: %s" % self.base_coupon_url)
        self.ele_wait(*self.add_base_coupon_button, 10)
        self.click_element(*self.add_base_coupon_button)
        log.info("已点击新增基础优惠券按钮")
        self.choose_coupon_type()
        self.ele_sleep(1)
        self.input_(*self.coupon_name, coupon_name)
        log.info("已输入基础优惠券名称: {}".format(coupon_name))
        self.input_(*self.coupon_price, coupon_price)
        log.info("已输入基础优惠券金额: {}".format(coupon_price))
        self.input_(*self.lowest_price, lowest_price)
        log.info("已输入最低消费金额: {}".format(lowest_price))

    def assert_result(self):
        self.ele_sleep(1)
        result = self.get_text(*self.toast)
        if "成功" in result:
            return True
        else:
            log.error(result)
            return False

    def add_base_coupon_all(self, coupon_name, coupon_price, lowest_price, remake):
        self.base_coupon_must(coupon_name, coupon_price, lowest_price)
        self.input_(*self.remake, remake)
        log.info("已添加备注")
        # ToDo: 点击确认按钮失败，无法找到元素
        self.click_element(*self.add_sure)
        log.info("已点击确认按钮")
        # if self.loctor(*self.error_msg):
        #     raise Exception(self.get_text(*self.error_msg))
        return self.assert_result()

    def add_base_coupon_must(self, coupon_name, coupon_price, lowest_price):
        self.base_coupon_must(coupon_name, coupon_price, lowest_price)
        # ToDo: 点击确认按钮失败，无法找到元素
        self.click_element(*self.add_sure)
        log.info("已点击确认按钮")
        # if self.loctor(*self.error_msg):
        #     raise Exception(self.get_text(*self.error_msg))
        return self.assert_result()

    def e_base_coupon_must(self, coupon_name):
        self.open_url(self.base_coupon_url)
        log.info("已打开优惠券管理页面，url为: %s" % self.base_coupon_url)
        self.click_element(*self.edit_base_coupon_button)
        log.info("已点击首个优惠券的编辑按钮")
        self.input_(*self.coupon_name, coupon_name)
        log.info("已修改基础优惠券名称: {}".format(coupon_name))

    def e_base_coupon_all(self, coupon_name, remake):
        self.e_base_coupon_must(coupon_name)
        self.input_(*self.remake, remake)
        log.info("已修改基础优惠券的备注字段: {}".format(remake))

    def edit_base_coupon_must(self, coupon_name):
        self.e_base_coupon_must(coupon_name)
        self.click_element(*self.add_sure)
        log.info("已点击%s按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    def edit_base_coupon_all(self, coupon_name, remake):
        self.e_base_coupon_all(coupon_name, remake)
        self.click_element(*self.add_sure)
        log.info("已点击%s按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    def del_base_coupon(self):
        try:
            self.ele_wait(*self.del_base_coupon_button, 5)
        except Exception:
            self.open_url(self.base_coupon_url)
        # self.refresh()
        self.ele_wait(*self.del_base_coupon_button, 8)
        self.click_element(*self.del_base_coupon_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.del_base_coupon_button))
        try:
            self.ele_sleep(1)
            self.click_element(*self.add_sure)
            log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
            self.ele_sleep(1)
        except Exception:
            self.ele_sleep(1)
            self.click_element(*self.second_sure)
            log.info("已点击 %s 按钮" % self.get_text(*self.second_sure))
            self.ele_sleep(1)
        log.info("已删除基础优惠券")
