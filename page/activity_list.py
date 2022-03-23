# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:create_activity
# DateTime:2022/3/17

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class CreateActivity(KeyWeb):
    # 活动列表界面url
    ac_list_url = base_url + "activity/activityList"
    # 活动名称搜索框
    ac_name_search = ("xpath", "//input[@placeholder='请输入活动名称']")
    # 查询按钮
    search_button = ("xpath", "//span[text()='查询']/..")
    # 编辑按钮
    edit_button = ("link text", "编辑")

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
    activity_type = ("xpath", "//span[@role='combobox']/span/span")
    activity_type_remove = ("xpath", "//span[contains(text(),'活动类型')]/../../..")
    search_input = ("xpath", "//input[@aria-label='filter select']")
    type_check = ("xpath", "//li[@role='treeitem']")
    activity_type_check_title = ("xpath", "//span[@class='ant-select-selection__rendered']/span")

    # 业务经理输入框，输入完后需要选择
    manager = ("xpath", "//div[@id='userName']/div/div")
    manager_input = ("xpath", "//div[@id='userName']/div/div")
    manager_check = ("xpath", "//li[@role='option']")
    manager_check_title = ("xpath", "//div[contains(text(),'业务经理')]/../div[2]")

    # 组织机构选择框
    organization_check = ("xpath", "//span[@id='customerId']/span/span")
    organization_direct_check = ("xpath", "(//li[@role='treeitem'])[15]")
    # 第一层箭头
    organization_one = ("xpath", "//li[@role='treeitem']/span")
    organization_one_have_type = ("xpath", "(//li[@role='treeitem']/span)[29]")
    # 第二层箭头
    organization_two = ("xpath", "//ul[@role='group']/li/span")
    # 第三层具体机构
    organization_three = ("xpath", "(//ul[@role='group'])[last()]/li")
    organization_check_title = ("xpath", "(//span[@class='ant-select-selection__rendered'])[2]/span")

    # 展开按钮
    expand_button = ("xpath", "//a[contains(text(), '展开')]")
    # 积分比率
    points = ("id", "integralRatio")
    # 订单失效时间
    order_end_time = ("id", "activityOrderOverdue")
    # 备注窗口切换
    # iframe = ("xpath", "//iframe[@allowtransparency='true']")
    # 备注输入框,输入完成后要切换回默认窗体
    remake = ("xpath", "//*[@id='tinymce']/p")

    # 活动图片上传
    img_check = ("xpath", "//div[@class='up_img']")
    img = ("xpath", "//div[@class='ant-card-cover']")
    img_sure = ("xpath", "(//span[contains(text(),'确')])[last()]")

    # 保存按钮
    save_button = ("xpath", "//span[contains(text(), '保存')]/..")
    # 提示语
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")

    def search_ac(self, search_ac_name):
        self.open_url(self.ac_list_url)
        log.info("已打开活动列表页面，url为: %s" % self.ac_list_url)
        self.input_(*self.ac_name_search, search_ac_name)
        log.info("活动名称搜索框中输入活动名称为: %s" % search_ac_name)
        self.click_element(*self.search_button)
        log.info("点击 %s 按钮" % self.get_text(*self.search_button))
        self.ele_sleep(1)
        try:
            log.info("点击 %s 按钮" % self.get_text(*self.edit_button))
            self.click_element(*self.edit_button)
        except Exception as e:
            log.error("没有符合条件的活动哦，请检查活动名称后重试")
            raise Exception(e)

    def deal_time(self):
        remove1_status = self.js_remove("readonly", *self.activity_start_time)
        remove2_status = self.js_remove("readonly", *self.activity_end_time)
        if not remove1_status:
            log.error("移除开始时间的只读属性失败啦")
        self.click_element(*self.activity_start_time)
        self.ele_sleep(1)
        self.click_element(*self.now)
        start_date = self.get_attribute(*self.now, "title")
        log.info("已选择活动开启时间为{}".format(start_date))

        if not remove2_status:
            log.error("移除结束时间的只读属性失败啦")
        self.click_element(*self.activity_end_time)
        self.click_element(*self.time_check)
        self.ele_sleep(1)
        self.click_element(*self.sure)
        end_date = self.get_attribute(*self.time_check, "title")
        log.info("已选择活动结束时间为{}".format(end_date))

    def deal_type(self, ac_type=None):
        # TODO: 移除无法点击元素属性尝试，失败了
        # try:
        #     self.mouse_click(*self.activity_type)
        #     log.info("已点击活动类型选择框")
        # except Exception as e:
        #     self.js_remove(*self.activity_type_remove, text="aria-disabled='true'")
        #     self.js_set(*self.activity_type_remove, att_name='class', att_value='ant-select ant-select-enabled')
        #     log.warning(e)
        #     self.mouse_click(*self.activity_type)
        #     log.info("已点击活动类型选择框")
        self.mouse_click(*self.activity_type)
        log.info("已点击活动类型选择框")
        if ac_type is not None:
            self.input_(*self.search_input, ac_type)
        try:
            self.click_element(*self.type_check)
            log.info("已选择活动类型 {} 啦".format(self.get_attribute(*self.activity_type_check_title, "title")))
        except Exception:
            log.error("没有活动类型可以选择哦")
            return False

    def deal_manager(self, ac_manager=None):
        self.ele_sleep(1)
        self.click_element(*self.manager)
        log.info("已点击业务经理选择框")
        if ac_manager is not None:
            self.mouse_input(*self.manager_input, ac_manager)
        try:
            self.click_element(*self.manager_check)
            log.info("已选择业务经理 {} 啦".format(self.get_attribute(*self.manager_check_title, "title")))
        except Exception:
            log.error("没有业务经理可以选择哦")
            return False

    def deal_organization(self, ac_organization=None):
        """
            根据是否触发过活动类型来进行选择，如果没触发过，可以直接使用类型里的元素，如果触发过，则使用组织机构自己的元素
        """
        self.click_element(*self.organization_check)
        log.info("已点击组织机构选择框")
        if ac_organization is not None:
            self.input_(*self.search_input, ac_organization)
        # 银联只能选择三级机构
        try:
            self.js_click(*self.organization_one)
            log.info("尝试点击第一个箭头")
            if self.loctor(*self.organization_two):
                pass
            else:
                self.js_click(*self.organization_one_have_type)
                if self.loctor(*self.organization_two):
                    pass
                else:
                    raise Exception("点击一级机构的箭头失败")
            self.js_click(*self.organization_two)
            log.info("尝试点击第二个箭头")
            self.mouse_click(*self.organization_three)
            log.info("选择三级机构")
            self.ele_sleep(1)
        except Exception:
            # 未触发活动类型时进行选择,点击首个机构
            self.click_element(*self.type_check)
            if self.get_attribute(*self.organization_check_title, "title") is not None:
                log.info("已选择组织机构 {} 啦".format(self.get_attribute(*self.organization_check_title, "title")))
            else:
                try:
                    # 触发了活动类型进行选择，点击首个机构
                    self.click_element(*self.organization_direct_check)
                    log.info("已选择组织机构 {} 啦".format(self.get_attribute(*self.organization_check_title, "title")))
                except Exception as e:
                    log.error("没有组织机构可以选择哦")
                    return e

    def save(self):
        self.ele_sleep(1)
        self.click_element(*self.save_button)
        log.info("已点击 %s 按钮" % self.get_text(*self.save_button))

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

    def more_create(self, remake_text, points_num=None, order_time=None):
        self.click_element(*self.expand_button)
        log.info("已点击展开按钮")

        if points_num is not None:
            self.mouse_clear_input(*self.points, points_num)
            log.info("已输入积分比率 {}".format(points_num))
        if order_time is not None:
            self.mouse_clear_input(*self.order_end_time, order_time)
            log.info("已输入订单取消时长")
        # self.ele_sleep(1)
        self.switch_frame(name="xpath", value="//iframe[@allowtransparency='true']")
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

    def activity_must(self, ac_name, ac_title, ac_type=None, ac_manager=None, ac_organization=None):
        self.ele_sleep(1)
        self.input_(*self.activity_name, ac_name)
        log.info("已输入活动名称：{}".format(ac_name))
        self.input_(*self.activity_title, ac_title)
        log.info("已输入活动标题：{}".format(ac_title))
        self.ele_sleep(1)
        self.deal_time()
        self.ele_sleep(1)
        self.deal_type(ac_type)
        self.ele_sleep(1)
        self.deal_manager(ac_manager)
        self.ele_sleep(1)
        self.deal_organization(ac_organization)

    def create_activity_must(self, ac_name, ac_title, ac_type=None, ac_manager=None, ac_organization=None):
        self.open_url(self.create_url)
        log.info("已打开创建活动网址: {}".format(self.create_url))
        self.activity_must(ac_name, ac_title, ac_type, ac_manager, ac_organization)
        self.save()
        return self.assert_result()

    def create_activity_all(self, ac_name, ac_title, remake_text, ac_type=None, ac_manager=None, ac_organization=None,
                            points_num=None, order_time=None):
        self.open_url(self.create_url)
        log.info("已打开创建活动网址: {}".format(self.create_url))
        self.activity_must(ac_name, ac_title, ac_type, ac_manager, ac_organization)
        self.more_create(remake_text, points_num, order_time)
        self.deal_img()
        self.save()
        return self.assert_result()

    def edit_activity_must(self, search_ac_name, ac_name, ac_title, ac_type=None, ac_manager=None,
                           ac_organization=None):
        self.search_ac(search_ac_name)
        self.activity_must(ac_name, ac_title, ac_type, ac_manager, ac_organization)
        self.save()
        return self.assert_result()

    def edit_activity_all(self, search_ac_name, ac_name, ac_title, remake_text, ac_type=None, ac_manager=None,
                          ac_organization=None, points_num=None, order_time=None):
        self.search_ac(search_ac_name)
        self.activity_must(ac_name, ac_title, ac_type, ac_manager, ac_organization)
        self.more_create(remake_text, points_num, order_time)
        self.deal_img()
        self.save()
        return self.assert_result()
