# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : coupon_label_list.py
from selenium.webdriver import Keys

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class CouponLabelList(KeyWeb):
    coupon_label_url = base_url + "coupons/LabelInfoList"

    # 新增按钮
    add_button = ("xpath", "//span[text()='新增']/..")
    # 活动名称输入选择框
    ac_name = ("xpath", "//div[@id='activityId']/div/div")
    # 第一个符合条件的选项
    ac_name_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])")
    # 标签名称
    label_name = ("id", "labelName")
    # 标签优先级
    label_priority = ("id", "labelPriority")
    # 标签计算逻辑
    label_logic = ("id", "labelLogic")
    # 确定按钮
    sure_button = ("xpath", "//span[text()='确 定']/..")

    # 编辑按钮
    edit_button = ("link text", "编辑")

    # 删除按钮
    delete_button = ("link text", "删除")
    del_sure = ("xpath", "(//span[text()='确 定']/..)[2]")

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

    def add_label(self, ac_name, label_name, label_priority, label_logic):
        self.open_url(self.coupon_label_url)
        log.info("已打开优惠券批次管理页面，url为: %s" % self.coupon_label_url)
        self.click_element(*self.add_button)
        log.info("点击 %s 按钮" % self.get_text(*self.add_button))
        self.move_ele(*self.ac_name)
        self.mouse_double_click(*self.ac_name)
        self.ele_sleep(1)
        self.mouse_input(*self.ac_name, ac_name)
        log.info("输入活动名称：{}".format(ac_name))
        try:
            self.click_element(*self.ac_name_first)
            log.info("选择下拉列表中第一个活动: {}".format(self.get_text(*self.ac_name_first)))
        except Exception as e:
            log.error("没有符合条件的活动！请检查活动名称再次重试")
            return e
        self.input_(*self.label_name, label_name)
        log.info("已输入标签名称: {}".format(label_name))

        self.ele_sleep(1)
        self.mouse_input(*self.label_priority, label_priority)
        log.info("已输入标签优先级: {}".format(label_priority))

        self.input_(*self.label_logic, label_logic)
        log.info("已输入标签计算逻辑: {}".format(label_logic))
        self.click_element(*self.sure_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.sure_button))
        return self.assert_result()

    def edit_label(self, label_name, label_priority, label_logic):
        self.click_element(*self.edit_button)
        log.info("点击 %s 按钮" % self.get_text(*self.edit_button))
        self.mouse_clear_input(*self.label_name, label_name)
        log.info("已修改标签名称: {}".format(label_name))

        self.ele_sleep(1)
        self.mouse_clear_input(*self.label_priority, label_priority)
        log.info("已修改标签优先级: {}".format(label_priority))

        self.clear_input(*self.label_logic, label_logic)
        log.info("已修改标签计算逻辑: {}".format(label_logic))
        self.click_element(*self.sure_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.sure_button))
        return self.assert_result()

    def delete_label(self):
        self.click_element(*self.delete_button)
        log.info("点击 %s 按钮" % self.get_text(*self.delete_button))
        self.click_element(*self.del_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.del_sure))
        return self.assert_result()
