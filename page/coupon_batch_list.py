# -*- coding: utf-8 -*-
# @Time    : 2022/3/21
# @Author  : 阿宋
# @File    : coupon_batch_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class CouponBatchList(KeyWeb):
    coupon_batch_url = base_url + "coupons/CouponBatchList"
    # 发券活动查询
    send_ac_search = ("xpath", "//div[@class='ant-select-selection__rendered']")
    send_ac_input = ("xpath", "//div[@class='ant-select-search__field__wrap']")
    send_ac_search_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])")
    # 查询按钮
    search_button = ("xpath", "//span[text()='查询']/..")
    # 商品更改按钮
    edit_goods_button = ("link text", "商品更改")
    # 新增按钮
    add_button = ("xpath", "//span[text()='新增']/..")
    # 新增第一个商品
    add_first_goods = ("xpath", "//td[@class='ant-table-selection-column']")
    # 新增确定按钮,由于先尝试删除再新增，所以新增确定按钮序列为4，否则为3,这里用last最后一个尝试
    add_sure = ("xpath", "(//span[text()='确 定']/..)[last()]")
    # 删除按钮
    delete_button = ("link text", "删除")
    # 删除确定按钮
    del_sure = ("xpath", "(//span[text()='确 定']/..)[3]")
    # 提示语文本
    toast = ("xpath", "//div[@class='ant-message']/span/div/div/div/span")

    def search_ac_cp(self, ac_name):
        self.open_url(self.coupon_batch_url)
        log.info("已打开优惠券批次管理页面，url为: %s" % self.coupon_batch_url)
        self.move_ele(*self.send_ac_search)
        self.mouse_double_click(*self.send_ac_search)
        self.ele_sleep(1)
        self.mouse_input(*self.send_ac_input, ac_name)
        log.info("输入发券活动名：{}".format(ac_name))
        self.click_element(*self.send_ac_search_first)
        log.info("选择下拉列表中第一个活动: {}".format(self.get_text(*self.send_ac_search_first)))
        self.click_element(*self.search_button)
        log.info("点击 %s 按钮" % self.get_text(*self.search_button))

    def assert_result(self):
        self.ele_sleep(1)
        result = self.get_text(*self.toast)
        if "成功" in result:
            return True
        else:
            log.error(result)
            return False

    def edit_goods(self):
        self.ele_sleep(3)
        self.click_element(*self.edit_goods_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.edit_goods_button))
        try:
            self.click_element(*self.delete_button)
            log.info("已点击 %s 按钮" % self.get_text(*self.delete_button))
            self.click_element(*self.del_sure)
            log.info("已点击 %s 按钮" % self.get_text(*self.del_sure))
            return self.assert_result()
        except Exception:
            self.click_element(*self.add_button)
            log.info("已点击 %s 按钮" % self.get_text(*self.add_button))
            self.click_element(*self.add_first_goods)
            log.info("已选择首个商品")
            self.click_element(*self.add_sure)
            log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
            return self.assert_result()

    def fix_cp_goods(self, ac_name):
        self.search_ac_cp(ac_name)
        return self.edit_goods()
