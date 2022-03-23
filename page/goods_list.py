# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:add_goods
# DateTime:2022/3/17

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log_color import HandleLog

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = HandleLog()


class AddGoods(KeyWeb):
    """
        由于创建活动的选择活动类型无法成功，所以暂时做一个活动列表搜索指定活动进行添加商品操作
        1. 打开活动列表界面
        2. 搜索活动名称
        3.点击搜索
        4.点击编辑
    """
    # 活动列表界面url
    ac_list_url = base_url + "activity/activityList"
    # 活动名称搜索框
    ac_name_search = ("xpath", "//input[@placeholder='请输入活动名称']")
    # 查询按钮
    search_button = ("xpath", "//span[text()='查询']/..")
    # 编辑按钮
    edit_button = ("link text", "编辑")

    # 商品信息页
    goods_info_tab = ("xpath", "//div[contains(text(), '商品信息')]")
    # 录入按钮
    add_goods = ("xpath", "//span[text()='录入']/..")
    # 产品名称选择框
    product_name_check = ("xpath", "//div[@id='productId']/div/div")
    # 产品勾选按钮
    product_check = ("xpath", "//td[@class='ant-table-selection-column'][1]")
    # 产品弹窗确定按钮
    product_sure = ("xpath", "(//span[contains(text(),'确')])[last()]")
    # 合同价
    contract_price = ("id", "goodsContractPrice")
    # 现金价格
    cash_price = ("id", "goodsCashPrice")
    # 积分价格
    points_price = ("id", "goodsPointsPrice")
    # 总投放量
    all_input = ("id", "goodsAmountInput")
    # 库存报警数量，可以选择不填，存在默认值
    war_input = ("id", "goodsMinAmount")
    # 添加商品弹窗的确定按钮
    add_sure = ("xpath", "(//span[contains(text(),'确')])[1]")

    # 活动图片上传
    img_check = ("xpath", "(//div[@class='up_img'])[2]")
    img_check_1 = ("xpath", "(//div[@class='up_img'])[last()]")
    img = ("xpath", "//div[@class='ant-card-cover']")
    img_sure = ("xpath", "(//span[contains(text(),'确')])[last()]")

    # 展开按钮
    expand_button = ("xpath", "(//div[@class='ant-col ant-col-3']/a)[last()]")

    # 推荐理由
    recommend = ("id", "goodsDisp2")

    # 商品详情窗口切换
    iframe = ("xpath", "//div[@class='tox-edit-area']/iframe")
    # 商品详情输入框,输入完成后要切换回默认窗体
    goods_info = ("xpath", "//*[@id='tinymce']/p")

    # 备注
    remake = ("id", "goodsComment")

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

    def deal_img(self):
        self.click_element(*self.img_check)
        log.info("已点击小图标选择框")
        self.click_element(*self.img)
        log.info("已选择第一张图片")
        self.js_click(*self.img_sure)
        log.info("已点击确定按钮")

    def deal_img1(self):
        self.click_element(*self.img_check_1)
        log.info("已点击多图标选择框")
        self.click_element(*self.img)
        log.info("已选择第一张图片")
        self.js_click(*self.img_sure)
        log.info("已点击确定按钮")

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

    def create_must(self, contract_price, cash_price, points_price, all_input_num, war_input_num=None):

        self.click_element(*self.goods_info_tab)
        log.info("已点击商品信息标签页")
        self.ele_sleep(2)
        self.click_element(*self.add_goods)
        log.info("已点击录入商品按钮")
        self.ele_sleep(2)
        self.mouse_click(*self.product_name_check)
        log.info("已点击产品选择框")
        self.ele_sleep(2)
        self.mouse_click(*self.product_check)
        log.info("已点击产品选择按钮")
        self.js_click(*self.product_sure)
        log.info("已点击产品弹窗的确定按钮")

        self.mouse_input(*self.contract_price, contract_price)
        log.info("已输入商品的合同价: %s" % contract_price)
        self.mouse_input(*self.cash_price, cash_price)
        log.info("已输入商品的现金价格: %s" % cash_price)
        self.mouse_input(*self.points_price, points_price)
        log.info("已输入商品的积分价格: %s" % points_price)

        self.mouse_input(*self.all_input, all_input_num)
        log.info("已输入商品的投放数量: %s" % all_input_num)
        if war_input_num is not None:
            self.mouse_input(*self.war_input, war_input_num)

    def create_goods(self, search_ac_name, contract_price, cash_price, points_price, all_input_num, war_input_num=None):
        # TODO:暂时添加的搜索活动名称进行添加商品操作
        self.search_ac(search_ac_name)
        self.ele_sleep(2)
        self.create_must(contract_price, cash_price, points_price, all_input_num, war_input_num)
        self.js_click(*self.add_sure)
        log.info("已点击添加商品弹窗保存按钮")
        return self.assert_result()

    def create_all_goods(self, search_ac_name, contract_price, cash_price, points_price, all_input_num, recommend, remake,
                         goods_info, war_input_num=None):
        self.search_ac(search_ac_name)
        self.create_must(contract_price, cash_price, points_price, all_input_num, war_input_num)
        self.ele_sleep(3)
        self.deal_img()
        self.click_element(*self.expand_button)
        log.info("已点击展开按钮")
        self.deal_img1()
        self.input_(*self.recommend, recommend)
        log.info("已输入商品的推荐理由: %s" % recommend)
        self.input_(*self.remake, remake)
        log.info("已输入商品的备注: %s" % remake)

        self.switch_frame(name="xpath", value="(//iframe[@allowtransparency='true'])[2]")
        self.input_(*self.goods_info, goods_info)
        log.info("已输入商品详情: %s" % goods_info)
        self.default()

        self.js_click(*self.add_sure)
        log.info("已点击添加商品弹窗保存按钮")
        return self.assert_result()
