# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:create_activity
# DateTime:2022/3/17

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log import log

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = log()


class CreateActivity(KeyWeb):
    create_url = base_url + "activity/createActivitiy"
    activity_name = ("id", "activityName")
    activity_title = ("id", "activityTitle")

    # 需要移除readonly=True属性
    activity_start_time = ("xpath", "//input[@placeholder='请选择日期']")
    activity_end_time = ("xpath", "(//input[@placeholder='请选择日期'])[last()]")
    now = ("xpath", "//a[contains(text(), '此刻')]")
    time_check = ("xpath", "(//tr[@role='row'])[last()]/td")
    sure = ("xpath", "//a[contains(text(), '确 定')]")

    # 活动类型选择框，点击后，出现下拉框，可以搜索或者默认选择第一个
    activity_type = ("xpath", "//span[contains(text(),'活动类型')]/..")
    search_input = ("xpath", "//input[@aria-label='filter select']")
    type_check = ("xpath", "//li[@role='treeitem']")

    # 业务经理输入框，输入完后需要选择
    manager = ("xpath", "//div[contains(text(),'业务经理')]/../..")
    manager_input = ("xpath", "//div[@unselectable='on']")
    manager_check = ("xpath", "//li[@role='option']")

    # 组织机构选择框，点击后，出现下拉框，可以搜索或者默认选择第一个(搜索和选择方法同活动类型处理)
    organization_check = ("xpath", "//span[contains(text(),'组织')]/../..")
    # 第一层箭头
    organization_one = ("xpath", "//li[@role='treeitem']/span")
    # 第二层箭头
    organization_two = ("xpath", "//ul[@role='group']/li/span")
    # 第三层具体机构
    organization_three = ("xpath", "(//ul[@role='group'])[last()]/li")

    # 展开按钮
    expand_button = ("xpath", "//div[@class='ant-col ant-col-3']/a")

    # 积分比率
    points = ("id", "integralRatio")

    # 订单失效时间
    order_end_time = ("id", "activityOrderOverdue")

    # 备注窗口切换
    iframe = ("xpath", "//div[@class='tox-edit-area']/iframe")

    # 备注输入框,输入完成后要切换回默认窗体
    remake = ("xpath", "//*[@id='tinymce']/p")

    # 活动图片上传
    img_check = ("xpath", "//div[@class='up_img']")
    img = ("xpath", "//div[@class='ant-card-cover']")
    img_sure = ("xpath", "(//span[contains(text(),'确')])[last()]")

    # 保存按钮
    save_button = ("xpath", "//span[contains(text(), '保存')]/..")

    # 提示语
    toast = ("xpath", "//div[@class='ant-message']/span/div/div/div/span")

    def deal_time(self):
        remove1_status = self.js_remove("readonly", *self.activity_start_time)
        remove2_status = self.js_remove("readonly", *self.activity_end_time)
        if not remove1_status:
            log.error("移除开始时间的只读属性失败啦")
        self.click_element(*self.activity_start_time)
        self.click_element(*self.now)
        log.info("已选择活动开启时间为当前时间啦")

        if not remove2_status:
            log.error("移除结束时间的只读属性失败啦")
        self.click_element(*self.activity_end_time)
        self.click_element(*self.time_check)
        self.ele_sleep(1)
        self.click_element(*self.sure)
        end_date = self.get_attribute(*self.time_check, "title")
        log.info("已选择活动结束时间为{}".format(end_date))

    def deal_type(self, ac_type=None):
        self.js_click(*self.activity_type)
        log.info("已点击活动类型选择框")
        if ac_type is not None:
            self.input_(*self.search_input, ac_type)
        try:
            self.click_element(*self.type_check)
            log.info("已选择活动类型啦")
        except Exception:
            log.error("没有活动类型可以选择哦")
            return False

    def deal_manager(self, ac_manager=None):
        self.click_element(*self.manager)
        log.info("已点击业务经理选择框")
        if ac_manager is not None:
            self.input_(*self.manager_input, ac_manager)
        try:
            self.click_element(*self.manager_check)
            log.info("已选择业务经理啦")
        except Exception:
            log.error("没有业务经理可以选择哦")
            return False

    def deal_organization(self, ac_organization=None):
        self.click_element(*self.organization_check)
        log.info("已点击组织机构选择框")
        if ac_organization is not None:
            self.input_(*self.search_input, ac_organization)
        try:
            # 银联只能选择三级机构
            self.click_element(*self.type_check)
            if self.loctor(*self.organization_one):
                self.js_click(*self.organization_one)
                if self.loctor(*self.organization_two):
                    self.js_click(*self.organization_two)
                    self.js_click(*self.organization_three)
            self.click_element(*self.type_check)
            log.info("已选择组织机构啦")
        except Exception as e:
            log.error(e)
            log.error("没有组织机构可以选择哦")
            return False

    def save(self):
        self.click_element(*self.save_button)
        log.info("已点击保存按钮")
        result = self.get_text(*self.toast)
        if "成功" in result:
            return True
        else:
            log.error(result)
            return False

    def more_create(self, remake_text, points_num=None, order_time=None):
        self.click_element(*self.expand_button)
        log.info("已点击展开按钮")

        if points_num is not None:
            self.input_(*self.points, points_num)
            log.info("已输入积分比率")
        if order_time is not None:
            self.input_(*self.order_end_time, order_time)
            log.info("已输入订单取消时长")
        # self.ele_sleep(1)
        # Todo：无法切换至iframe
        self.switch_frame(*self.iframe)
        self.input_(*self.remake, remake_text)
        log.info("已填写完备注信息")
        self.default()

    def deal_img(self):
        self.click_element(*self.img_check)
        log.info("已点击活动图片选择框")
        self.click_element(*self.img)
        log.info("已选择第一张图片")
        self.js_click(*self.img_sure)
        log.info("已点击确定按钮")

    def create_activity_must(self, ac_name, ac_title, ac_type=None, ac_manager=None, ac_organization=None):
        self.open_url(self.create_url)
        log.info("已打开创建活动网址{}".format(self.create_url))

        self.input_(*self.activity_name, ac_name)
        log.info("已输入活动名称：{}".format(ac_name))

        self.input_(*self.activity_title, ac_title)
        log.info("已输入活动标题：{}".format(ac_title))

        self.deal_time()

        self.deal_type(ac_type)

        self.deal_manager(ac_manager)

        self.deal_organization(ac_organization)

        return self.save()

    def create_activity_all(self, ac_name, ac_title, remake_text, ac_type=None, ac_manager=None, ac_organization=None,
                            points_num=None, order_time=None):
        self.open_url(self.create_url)
        log.info("已打开创建活动网址{}".format(self.create_url))

        self.input_(*self.activity_name, ac_name)
        log.info("已输入活动名称：{}".format(ac_name))

        self.input_(*self.activity_title, ac_title)
        log.info("已输入活动标题：{}".format(ac_title))

        self.deal_time()

        self.deal_type(ac_type)

        self.deal_manager(ac_manager)

        self.deal_organization(ac_organization)

        self.more_create(remake_text, points_num, order_time)

        self.deal_img()

        return self.save()
