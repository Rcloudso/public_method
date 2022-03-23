# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : exchange_code_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class ExchangeCodeList(KeyWeb):
    url = base_url + "exchange/ExchangeList"
    # 发券活动查询
    send_ac_search = ("xpath", "//div[@class='ant-select-selection__rendered']")
    send_ac_input = ("xpath", "//div[@class='ant-select-search__field__wrap']")
    send_ac_search_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])")
    # 查询按钮
    main_search_button = ("xpath", "//span[text()='查询']/..")

    # 更改有效期按钮
    edit_time = ("link text", "有效期更改")
    effect_time = ("xpath", "//input[@placeholder='请选择日期']")
    fail_time = ("xpath", "(//input[@placeholder='请选择日期'])[2]")

    # 生成兑换码
    create_exchange = ("xpath", "//span[text()='生成兑换码']/..")
    exchange_sure = ("xpath", "//span[text()='确 定']/..")

    # 基础兑换码选择按钮
    base_exchange_choose = ("xpath", "//div[@id='couponNameId']/div/div")
    search_exchange = ("xpath", "(//input[@placeholder='请输入兑换码名称'])[2]")
    search_button = ("xpath", "(//span[text()='查询']/..)[2]")
    first_base_exchange = ("xpath", "//td[@class='ant-table-selection-column']")
    base_exchange_sure = ("xpath", "(//span[text()='确 定']/..)[2]")

    # 发码活动输入选择框
    send_ac = ("xpath", "//div[@id='activityId']/div/div")
    send_ac_first = ("xpath", "//*[@id='test-uuid']/ul/li[1]")
    # 用码活动输入选择框
    use_ac = ("xpath", "//div[@id='applyActivityId']/div/div")
    use_ac_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])[2]")

    # 生成数量输入框
    builds_num = ("xpath", "//input[@placeholder='请输入生成数量']")

    # 时间框处理，需要移除readonly=True属性
    start_time = ("xpath", "//input[@placeholder='请选择生效时间']")
    end_time = ("xpath", "//input[@placeholder='请选择失效时间']")
    now = ("link text", "此刻")
    time_check = ("xpath", "(//tr[@role='row'])[last()]/td")
    time_sure = ("link text", "确 定")

    # 可兑换商品选择
    exchange_goods = ("xpath", "//div[@id='couponGoods']/div/div")
    exchange_goods_last = ("xpath", "(//td[@class='ant-table-selection-column'])[last()]")
    exchange_goods_sure = ("xpath", "(//span[text()='确 定']/..)[3]")

    # 提示语文本
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")

    def search_ac_cp(self, ac_name):
        self.move_ele(*self.send_ac_search)
        self.mouse_double_click(*self.send_ac_search)
        self.ele_sleep(1)
        self.mouse_input(*self.send_ac_input, ac_name)
        log.info("输入发码活动名：{}".format(ac_name))
        try:
            self.click_element(*self.send_ac_search_first)
            log.info("选择下拉列表中第一个活动: {}".format(self.get_text(*self.send_ac_search_first)))
        except Exception as e:
            log.error("没有符合条件的活动！请检查活动名称再次重试")
            log.error(e)
        self.click_element(*self.main_search_button)
        log.info("点击 %s 按钮" % self.get_text(*self.main_search_button))

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

    def choose_base(self, exchange_name):
        # 选择基础券的业务逻辑
        self.ele_sleep(1)
        self.mouse_click(*self.base_exchange_choose)
        log.info("已点击基础券选择")
        self.mouse_input(*self.search_exchange, exchange_name)
        log.info("已输入兑换码名称 %s 准备进行搜索" % exchange_name)
        self.click_element(*self.search_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.search_button))
        self.ele_sleep(2)
        try:
            self.js_click(*self.first_base_exchange)
            log.info("已选择第一种基础兑换码")
        except Exception as error:
            log.error("没有符合条件的兑换码，请检查后重试！")
            raise error
        self.click_element(*self.base_exchange_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.base_exchange_sure))

    def check_ac(self, send_ac, use_ac):
        self.ele_sleep(2)
        self.click_element(*self.send_ac)
        self.mouse_input(*self.send_ac, send_ac)
        log.info("已输入发券活动: %s" % send_ac)
        self.ele_sleep(1)
        try:
            self.js_click(*self.send_ac_first)
            log.info("已选择第一个符合条件的活动")
        except Exception as e:
            log.error("没有匹配的活动！请检查活动名称")
            raise e
        self.click_element(*self.use_ac)
        self.mouse_input(*self.use_ac, use_ac)
        log.info("已输入适用活动: %s" % use_ac)
        self.ele_sleep(1)
        try:
            self.js_click(*self.use_ac_first)
            log.info("已选择第一个符合条件的活动")
        except Exception as e:
            log.error("没有匹配的活动！请检查活动名称")
            raise e

    def deal_time(self):
        self.ele_sleep(1)
        remove1_status = self.js_remove("readonly", *self.start_time)
        remove2_status = self.js_remove("readonly", *self.end_time)
        if not remove1_status:
            log.error("移除生效时间的只读属性失败啦")
        self.click_element(*self.start_time)
        self.ele_sleep(1)
        self.click_element(*self.now)
        start_date = self.get_attribute(*self.now, "title")
        log.info("已选择生效时间为{}".format(start_date))

        if not remove2_status:
            log.error("移除失效时间的只读属性失败啦")
        # self.click_element(*self.end_time)
        self.click_element(*self.time_check)
        self.ele_sleep(1)
        end_date = self.get_attribute(*self.time_check, "title")
        log.info("已选择失效时间为{}".format(end_date))
        log.info("点击 %s 按钮" % self.get_text(*self.time_sure))
        self.click_element(*self.time_sure)

    def check_goods(self):
        self.ele_sleep(2)
        self.mouse_click(*self.exchange_goods)
        log.info("已点击可兑换商品选择窗口")
        try:
            self.ele_sleep(1)
            self.mouse_click(*self.exchange_goods_last)
            log.info("点击商品列表中符合条件的商品")
        except Exception as e:
            log.error("没有符合条件的商品！请确保基础券与商品能够对应！")
            raise e
        self.ele_sleep(1)
        self.click_element(*self.exchange_goods_sure)

    # 生成兑换码业务主流程
    def create_exchange_code(self, exchange_name, send_ac, use_ac, builds_num):
        self.open_url(self.url)
        log.info("已打开兑换码管理页面，url为: %s" % self.url)
        self.click_element(*self.create_exchange)
        log.info("点击 %s 按钮" % self.get_text(*self.create_exchange))
        self.choose_base(exchange_name)
        self.check_ac(send_ac, use_ac)
        self.mouse_input(*self.builds_num, builds_num)
        log.info("输入生成的数量为 %s" % builds_num)
        self.deal_time()
        self.check_goods()
        self.click_element(*self.exchange_sure)
        log.info("点击 %s 按钮" % self.get_text(*self.exchange_sure))
        return self.assert_result()

    # 修改兑换码有效期主流程
    def edit_exchange_code_time(self, ac_name):
        self.open_url(self.url)
        log.info("已打开兑换码管理页面，url为: %s" % self.url)
        self.search_ac_cp(ac_name)
        self.ele_sleep(1)
        log.info("点击 %s 按钮" % self.get_text(*self.edit_time))
        self.click_element(*self.edit_time)

        remove1_status = self.js_remove("readonly", *self.effect_time)
        remove2_status = self.js_remove("readonly", *self.fail_time)
        if not remove1_status:
            log.error("移除生效时间的只读属性失败啦")
        self.click_element(*self.effect_time)
        self.ele_sleep(1)
        self.click_element(*self.now)
        start_date = self.get_attribute(*self.now, "title")
        log.info("已选择生效时间为{}".format(start_date))

        if not remove2_status:
            log.error("移除失效时间的只读属性失败啦")
        self.click_element(*self.fail_time)
        self.click_element(*self.time_check)
        self.ele_sleep(1)
        end_date = self.get_attribute(*self.time_check, "title")
        log.info("已选择失效时间为{}".format(end_date))
        log.info("点击 %s 按钮" % self.get_text(*self.time_sure))
        self.click_element(*self.time_sure)
        log.info("点击 %s 按钮" % self.get_text(*self.exchange_sure))
        self.click_element(*self.exchange_sure)
        return self.assert_result()
