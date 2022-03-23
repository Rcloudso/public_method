# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : phone_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class PhoneList(KeyWeb):
    phone_list_url = base_url + "basics/PhonesList"

    # 手机号搜索输入框
    search_phone_input = ("xpath", "//input[@placeholder='请输入手机号段']")
    # 查询按钮
    main_search_button = ("xpath", "//span[text()='查询']/..")

    # 新增按钮
    add_button = ("xpath", "//span[text()='新增']/..")
    # 手机号输入框
    phone_input = ("id", "number")
    # 运营商选择
    phone_type = ("xpath", "//div[@id='type']/div/div")
    # 具体运营商选择
    first_type = ("xpath", "//*[@id='test-uuid']/ul/li[1]")
    # 城市的选择
    city_check = ("xpath", "//span[@id='regionId']/span/span")
    # 首个省份的箭头
    first_row = ("xpath", "//li[@role='treeitem']/span")
    # 箭头下具体城市的选择,根据箭头展开的数据选择第一个
    row_city_check = ("xpath", "//*[@id='rc-tree-select-list_1']/ul/li/ul/li")
    row_city_check_title = ("xpath", "//*[@id='rc-tree-select-list_1']/ul/li/ul/li/span[2]")
    # 搜索城市名称
    city_search = ("xpath", "//*[@id='rc-tree-select-list_1']/span/span/input")
    # 搜索后的具体城市选择
    search_city_check = ("xpath", "(//li[@role='treeitem'])[last()]")
    add_sure = ("xpath", "//span[text()='确 定']/..")

    # 编辑按钮
    edit_button = ("link text", "编辑")

    # 删除按钮
    del_button = ("link text", "删除")

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

    def deal_city(self, city_name=None):
        self.ele_sleep(2)
        self.click_element(*self.city_check)
        log.info("已点击城市选择框")
        if city_name is not None:
            self.input_(*self.city_search, city_name)
            log.info("已在城市搜索框中搜索城市名：%s" % city_name)
            self.click_element(*self.search_city_check)
            log.info("已选择 %s 市" % self.get_attribute(*self.row_city_check_title, "title"))
        else:
            self.click_element(*self.first_row)
            log.info("已点击首个省份的小箭头")
            self.click_element(*self.row_city_check)
            log.info("已选择 %s 市" % self.get_attribute(*self.row_city_check_title, "title"))

    def search_phone(self, phone_number):
        self.open_url(self.phone_list_url)
        log.info("已打开手机号归属地页面，url为: %s" % self.phone_list_url)
        self.input_(*self.search_phone_input, phone_number)
        log.info("已输入手机号段为：%s" % phone_number)
        self.click_element(*self.main_search_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.main_search_button))

    # 添加手机号归属地业务流程
    def add_phone(self, phone_num, city_name=None):
        self.open_url(self.phone_list_url)
        log.info("已打开手机号归属地页面，url为: %s" % self.phone_list_url)
        self.click_element(*self.add_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_button))
        self.mouse_input(*self.phone_input, phone_num)
        log.info("已输入手机号段为：%s" % phone_num)
        self.click_element(*self.phone_type)
        log.info("已点击运营商选择窗口")
        self.click_element(*self.first_type)
        log.info("已选择首个运营商：%s" % self.get_text(*self.first_type))
        self.deal_city(city_name)
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    # 编辑手机号归属地业务流程
    def edit_phone(self, phone_number, phone_num, city_name=None):
        self.search_phone(phone_number)
        self.ele_wait(*self.edit_button)
        self.click_element(*self.edit_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.edit_button))
        self.ele_sleep(1)
        self.mouse_clear_input(*self.phone_input, phone_num)
        log.info("已输入新的手机号段为：%s" % phone_num)
        self.click_element(*self.phone_type)
        log.info("已点击运营商选择窗口")
        self.click_element(*self.first_type)
        log.info("已选择首个运营商：%s" % self.get_text(*self.first_type))
        self.deal_city(city_name)
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    def del_phone(self, phone_number):
        self.search_phone(phone_number)
        self.click_element(*self.del_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.del_button))
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()
