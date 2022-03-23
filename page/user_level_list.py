# -*- coding: utf-8 -*-
# @Time    : 2022/3/23
# @Author  : 阿宋
# @File    : user_level_list.py

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class UserLevelList(KeyWeb):
    user_level_url = base_url + "basics/ShUserLevelList"

    # 活动名称搜索款
    ac_search = ("xpath", "//div[@class='ant-select-selection__rendered']")
    ac_input = ("xpath", "//div[@class='ant-select-search__field__wrap']")
    ac_search_first = ("xpath", "(//*[@id='test-uuid']/ul/li[1])")
    # 查询按钮
    main_search_button = ("xpath", "//span[text()='查询']/..")

    # 新增按钮
    add_button = ("xpath", "//span[text()='新增']/..")
    # 活动名称输入选择框
    ac_input_check = ("xpath", "//div[@id='activityId']/div/div")
    # 活动选择
    ac_check = ("xpath", "//li[@role='option']")
    # 触发类型选择
    type_check = ("xpath", "//div[@id='type']/div/div")
    # 具体类型选择
    add_first_type = ("xpath", "(//*[@id='test-uuid']/ul/li[1])[2]")
    # 用户等级
    level = ("id", "level")
    # 手机号
    phone = ("id", "telphone")
    # 手机号md5值
    phone_md5 = ("id", "blackTelphoneMd5")
    # 身份证号
    card_id = ("id", "cardId")
    # 身份证号md5值
    card_id_md5 = ("id", "blackCardIdMd5")
    # 备注
    remake = ("id", "comment")
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

    def search_ac_cp(self, ac_name):
        self.open_url(self.user_level_url)
        log.info("已打开用户等级管理页面，url为: %s" % self.user_level_url)
        self.move_ele(*self.ac_search)
        self.mouse_double_click(*self.ac_search)
        self.ele_sleep(1)
        self.mouse_input(*self.ac_input, ac_name)
        log.info("输入活动名：{}".format(ac_name))
        try:
            self.click_element(*self.ac_search_first)
            log.info("选择下拉列表中第一个活动: {}".format(self.get_text(*self.ac_search_first)))
        except Exception as e:
            log.error("没有符合条件的活动！请检查活动名称再次重试")
            raise e
        self.click_element(*self.main_search_button)
        log.info("点击 %s 按钮" % self.get_text(*self.main_search_button))

    def deal_ac(self, ac_name):
        self.click_element(*self.ac_input_check)
        self.ele_sleep(1)
        self.mouse_input(*self.ac_input_check, ac_name)
        log.info("已输入发券活动")
        self.ele_sleep(2)
        try:
            self.js_click(*self.ac_check)
            log.info("已选择第一个符合条件的活动")
        except Exception as e:
            log.error("没有匹配的活动！请检查活动名称")
            raise e

    def deal_all(self, level, phone, phone_md5, card_id, card_id_md5, remake):
        self.click_element(*self.type_check)
        log.info("点击类型选择窗体")
        self.ele_sleep(1)
        self.click_element(*self.add_first_type)
        log.info("点击 %s 类型" % self.get_text(*self.add_first_type))
        self.ele_sleep(1)
        self.mouse_clear_input(*self.level, level)
        log.info("输入用户等级: %s" % level)
        self.ele_sleep(1)
        self.mouse_clear_input(*self.phone, phone)
        log.info("输入用户手机号: %s" % phone)
        self.ele_sleep(1)
        self.mouse_clear_input(*self.phone_md5, phone_md5)
        log.info("输入用户手机号md5值: %s" % phone_md5)
        self.ele_sleep(1)
        self.mouse_clear_input(*self.card_id, card_id)
        log.info("输入用户身份证号: %s" % card_id)
        self.ele_sleep(1)
        self.mouse_clear_input(*self.card_id_md5, card_id_md5)
        log.info("输入用户身份证号md5值: %s" % card_id_md5)
        self.ele_sleep(1)
        self.mouse_clear_input(*self.remake, remake)
        log.info("输入备注: %s" % remake)

    # 添加用户等级必填项业务流程
    def add_user_level_must(self, ac_name):
        self.open_url(self.user_level_url)
        log.info("已打开手机号归属地页面，url为: %s" % self.user_level_url)
        self.click_element(*self.add_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_button))
        self.deal_ac(ac_name)
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    # 添加用户等级全部业务流程
    def add_user_level_all(self, ac_name, level, phone, phone_md5, card_id, card_id_md5, remake):
        self.open_url(self.user_level_url)
        log.info("已打开手机号归属地页面，url为: %s" % self.user_level_url)
        self.click_element(*self.add_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_button))
        self.deal_ac(ac_name)
        self.deal_all(level, phone, phone_md5, card_id, card_id_md5, remake)
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    # 编辑用户等级业务流程
    def edit_user_level(self, ac_name, level, phone, phone_md5, card_id, card_id_md5, remake):
        self.search_ac_cp(ac_name)
        self.click_element(*self.edit_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.edit_button))
        self.deal_all(level, phone, phone_md5, card_id, card_id_md5, remake)
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()

    # 删除用户等级业务
    def delete_user_level(self, ac_name):
        self.search_ac_cp(ac_name)
        self.click_element(*self.del_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.del_button))
        self.click_element(*self.add_sure)
        log.info("已点击 %s 按钮" % self.get_text(*self.add_sure))
        return self.assert_result()
