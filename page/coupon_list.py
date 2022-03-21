# -*- coding: utf-8 -*-
# @Time    : 2022/3/18
# @Author  : 阿宋
# @File    : coupon_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class CouponList(KeyWeb):
    coupon_url = base_url + "coupons/CouponList"
    # 发券活动查询
    send_ac_search = ("xpath", "//div[@class='ant-select-selection__rendered']")
    send_ac_input = ("xpath", "//div[@class='ant-select-search__field__wrap']")
    send_ac_search_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])")
    # 查询按钮
    search_button = ("xpath", "//span[text()='查询']/..")
    # 优惠券选择
    check_coupon = ("xpath", "//td[@class='ant-table-selection-column']")
    # 作废按钮
    del_coupon = ("xpath", "//span[text()='作废优惠券']/..")
    # 作废确定按钮
    del_sure = ("xpath", "//span[text()='确 定']/..")
    # 生成优惠券按钮
    add_button = ("xpath", "//span[text()='生成优惠券']/..")
    # 基础优惠券选择
    base_coupon = ("xpath", "//div[@class='ant-select ant-select-disabled']")
    # 选择第一个基础优惠券
    first_coupon = ("xpath", "//td[@class='ant-table-selection-column']/span/label")
    # 优惠券确定按钮
    coupon_sure = ("xpath", "(//span[text()='确 定']/..)[3]")
    # 发券活动输入
    send_ac = ("id", "activityId")
    # 发券活动选择
    send_ac_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])[6]")
    # 适用活动输入
    use_ac = ("id", "applyActivityId")
    # 适用活动选择
    use_ac_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])[7]")
    # 生成数量
    builds_num = ("xpath", "//input[@placeholder='请输入生成数量']")
    # 需要移除readonly=True属性
    start_time = ("xpath", "//input[@placeholder='请选择生效时间']")
    end_time = ("xpath", "//input[@placeholder='请选择失效时间']")
    now = ("xpath", "//a[contains(text(), '此刻')]")
    time_check = ("xpath", "(//tr[@role='row'])[last()]/td")
    sure = ("xpath", "//a[contains(text(), '确')]")
    # 添加确定
    add_sure = ("xpath", "(//span[text()='确']/..)[2]")
    # 提示语
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")

    def deal_search(self, send_ac_search):
        self.click_element(*self.send_ac_search)
        self.ele_sleep(2)
        self.input_(*self.send_ac_search, send_ac_search)
        log.info("已输入要查询的活动{}".format(send_ac_search))
        self.ele_wait(*self.send_ac_search_first, 10)
        self.click_element(*self.send_ac_search_first)
        log.info("已选择匹配活动列表中第一个活动")

    def deal_time(self):
        remove1_status = self.js_remove("readonly", *self.start_time)
        remove2_status = self.js_remove("readonly", *self.end_time)
        if not remove1_status:
            log.error("移除开始时间的只读属性失败啦")
        self.click_element(*self.start_time)
        self.click_element(*self.now)
        log.info("已选择活动开启时间为当前时间啦")
        if not remove2_status:
            log.error("移除结束时间的只读属性失败啦")
        self.click_element(*self.end_time)
        self.click_element(*self.time_check)
        self.ele_sleep(1)
        self.click_element(*self.sure)
        end_date = self.get_attribute(*self.time_check, "title")
        log.info("已选择活动结束时间为{}".format(end_date))

    def coupon_must(self, send_ac, use_ac, builds_num):
        self.open_url(self.coupon_url)
        log.info("已打开优惠券管理页面，url为: %s" % self.coupon_url)
        self.click_element(*self.add_button)
        log.info("已点击生成优惠券按钮")
        # Todo: 点击无效
        self.ele_sleep(2)
        self.click_element(*self.base_coupon)
        log.info("已点击基础券选择框")
        self.ele_sleep(1)
        self.click_element(*self.first_coupon)
        log.info("已点击第一张基础优惠券")
        self.ele_sleep(1)
        self.click_element(*self.coupon_sure)
        log.info("已点击基础优惠券弹窗的确定按钮")
        self.click_element(*self.send_ac)
        self.input_(*self.send_ac, send_ac)
        log.info("已输入发券活动")
        self.ele_sleep(2)
        try:
            self.js_click(*self.send_ac_first)
            log.info("已选择第一个符合条件的活动")
        except Exception as e:
            log.error("没有匹配的活动！请检查活动名称")
            raise e
        self.click_element(*self.use_ac)
        self.input_(*self.use_ac, use_ac)
        log.info("已输入适用活动")
        self.ele_sleep(2)
        try:
            self.js_click(*self.use_ac_first)
            log.info("已选择第一个符合条件的活动")
        except Exception as e:
            log.error("没有匹配的活动！请检查活动名称")
            raise e
        self.input_(*self.builds_num, builds_num)
        log.info("已输入生成数量{}".format(builds_num))

    def assert_result(self):
        self.ele_sleep(1)
        result = self.get_text(*self.toast)
        if "成功" in result:
            return True
        else:
            log.error(result)
            return False

    def add_coupon_must(self, send_ac, use_ac, builds_num):
        self.coupon_must(send_ac, use_ac, builds_num)
        self.deal_time()
        return self.assert_result()

    def search_ac_cp(self, ac_name):
        self.open_url(self.coupon_url)
        log.info("已打开优惠券管理页面，url为: %s" % self.coupon_url)
        self.move_ele(*self.send_ac_search)
        self.mouse_double_click(*self.send_ac_search)
        self.ele_sleep(1)
        self.mouse_input(*self.send_ac_input, ac_name)
        log.info("输入发券活动名：{}".format(ac_name))
        self.click_element(*self.send_ac_search_first)
        log.info("选择下拉列表中第一个活动: {}".format(self.get_text(*self.send_ac_search_first)))
        self.click_element(*self.search_button)
        log.info("点击 %s 按钮" % self.get_text(*self.search_button))

    def check_coupon_list(self):
        self.click_element(*self.check_coupon)
        log.info("勾选首个优惠券")
        self.click_element(*self.del_coupon)
        log.info("点击 %s 按钮" % self.get_text(*self.del_coupon))
        log.info("点击 %s 按钮" % self.get_text(*self.del_sure))
        self.click_element(*self.del_sure)

    def del_cp_coupon(self, ac_name):
        self.search_ac_cp(ac_name)
        self.check_coupon_list()
        return self.assert_result()
