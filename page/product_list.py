# -*- coding: UTF-8 -*-    
# Author:Worker 
# FileName:add_product
# DateTime:2022/3/17

from base.keys import KeyWeb
from read_config.Read_config import readconfig
from My_option.Log import log

path = "../Conf/config.ini"
base_url = readconfig(path, "CFCA_TEST", "base_url")

log = log()


class ProductList(KeyWeb):
    product_url = base_url + "resource/ShProductList"
    # 首个产品
    first_product = ("xpath", "(//span[@class='ant-checkbox'])[2]")
    # 上下架按钮
    up_down_button = ("xpath", "//span[text()='批量上下架']/..")
    # 新增按钮
    add_button = ("xpath", "//span[text()='新增']/..")
    # 产品大分类(点一下，再输入)
    big_class = ("id", "productType1")
    big_class_check = ("xpath", "//li[@role='option' and text()='红包']")
    # 产品ID
    product_id = ("xpath", "(//input[@placeholder='请输入产品ID'])[2]")
    # 产品名称
    product_name = ("xpath", "(//input[@placeholder='请输入产品名称'])[2]")
    # 产品中分类(逻辑与大分类保持一致)
    middle_class = ("id", "productType2")
    middle_class_check = ("xpath", "//li[@role='option' and text()='通用权益']")
    # 产品小分类(逻辑与大分类保持一致)
    small_class = ("id", "productType3")
    small_class_check = ("xpath", "//span[@title= '月卡']/..")
    # 供应商
    supplier = ("id", "source")
    # 供应商选择
    supplier_check = ("xpath", "//span[@title='网信']/..")
    # 商品分类
    product_class = ("id", "productType4")
    product_class_check = ("xpath", "//span[@title='商品分类']")
    # 官方市场原价
    offical_price = ("xpath", "//input[@placeholder='请输入官方市场原价']")
    # 充值方式
    recharge_method = ("id", "productCharge")
    recharge_method_check = ("xpath", "//span[@title='直冲']/..")
    # 商品库存数量
    goods_stock = ("xpath", "//input[@placeholder='请输入商品库存数量']")
    # 发券账户类型
    account_type = ("xpath", "//span[text()='手机号']/../span")
    # 购买须知
    need_now = ("xpath", "//input[@placeholder='请输入购买须知']")
    # 客服电话
    telephone = ("xpath", "//input[@placeholder='请输入客服电话']")
    # 账户资质信息
    account_msg = ("xpath", "//input[@placeholder='请输入商户资质信息']")
    # 品牌
    brand = ("xpath", "//input[@placeholder='请输入品牌']")
    # 门店适用链接
    store_url = ("xpath", "//input[@placeholder='请输入适用门店链接']")
    # 上下架确定按钮
    up_down_sure = ("xpath", "(//span[text()='确 定']/..)[last()]")
    # 增加产品确定按钮
    add_sure = ("xpath", "//span[text()='确 定']/..")
    # 提示语
    toast = ("xpath", "(//div[@class='ant-message']/span/div/div/div/span)[last()]")

    def product_must(self, product_id, product_name, offical_price):
        self.open_url(self.product_url)
        log.info("已打开产品管理页面，url为: %s" % self.product_url)
        self.click_element(*self.add_button)
        log.info("已点击%s按钮" % self.get_text(*self.add_button))
        self.ele_sleep(2)
        self.click_element(*self.big_class)
        log.info("已点击产品大分类选择框")
        self.ele_sleep(2)
        self.click_element(*self.big_class_check)
        log.info("已选择产品大分类")
        self.ele_sleep(2)
        self.input_(*self.product_id, product_id)
        log.info("已输入产品ID为 {}".format(product_id))
        self.ele_sleep(2)
        self.input_(*self.product_name, product_name)
        log.info("已输入产品名称为 {}".format(product_name))
        self.ele_sleep(2)
        self.click_element(*self.middle_class)
        log.info("已点击产品中分类输入框")
        self.ele_sleep(2)
        self.click_element(*self.middle_class_check)
        log.info("已选择产品中分类")
        self.ele_sleep(2)
        self.js_click(*self.product_class)
        log.info("已点击商品分类选择框")
        self.ele_sleep(2)
        self.js_click(*self.product_class_check)
        log.info("已选择商品分类")
        self.ele_sleep(2)
        self.input_(*self.offical_price, offical_price)
        log.info("已输入官方市场原价为 {}".format(offical_price))
        self.ele_sleep(2)
        self.click_element(*self.recharge_method)
        log.info("已点击充值方式选择框")
        self.ele_sleep(2)
        self.click_element(*self.recharge_method_check)
        log.info("已选择充值方式")
        self.ele_sleep(2)

    def product_all(self, stock_num, need_now, telephone, account_msg, brand, store_url):
        self.click_element(*self.small_class)
        log.info("已点击产品小分类输入框")
        self.ele_sleep(2)
        self.click_element(*self.small_class_check)
        log.info("已选择产品小分类")
        self.ele_sleep(2)
        self.click_element(*self.supplier)
        log.info("已点击供应商选择框")
        self.ele_sleep(2)
        self.click_element(*self.supplier_check)
        log.info("已选择供应商")
        self.ele_sleep(2)
        self.input_(*self.goods_stock, stock_num)
        log.info("已输入商品库存数量{}".format(stock_num))
        self.ele_sleep(2)
        self.js_click(*self.account_type)
        log.info("已选择发券账户类型")
        self.ele_sleep(2)
        self.input_(*self.need_now, need_now)
        log.info("已输入购买须知：{}".format(need_now))
        self.ele_sleep(2)
        self.input_(*self.telephone, telephone)
        log.info("已输入客服电话：{}".format(telephone))
        self.ele_sleep(2)
        self.input_(*self.account_msg, account_msg)
        log.info("已输入账户资质信息：{}".format(account_msg))
        self.ele_sleep(2)
        self.input_(*self.brand, brand)
        log.info("已输入品牌名：{}".format(brand))
        self.ele_sleep(2)
        self.input_(*self.store_url, store_url)
        log.info("已输入适用账户链接：{}".format(store_url))

    def assert_result(self):
        self.ele_sleep(2)
        result = self.get_text(*self.toast)
        if "成功" in result:
            return True
        else:
            log.error(result)
            return False

    def add_product_must(self, product_id, product_name, offical_price):
        self.product_must(product_id, product_name, offical_price)
        self.click_element(*self.add_sure)
        log.info("已点击确定按钮")
        return self.assert_result()

    def add_product_all(self, product_id, product_name, offical_price, stock_num, need_now, telephone, account_msg,
                        brand, store_url):
        self.product_must(product_id, product_name, offical_price)
        self.product_all(stock_num, need_now, telephone, account_msg, brand, store_url)
        self.click_element(*self.add_sure)
        log.info("已点击确定按钮")
        return self.assert_result()

    def updown_product(self):
        self.open_url(self.product_url)
        self.ele_wait(*self.first_product, text=10)
        self.js_click(*self.first_product)
        log.info("已点击第一个产品")
        self.click_element(*self.up_down_button)
        log.info("已点击批量上下架按钮")
        self.ele_wait(*self.up_down_sure, 10)
        self.click_element(*self.up_down_sure)
        log.info("已点击确定按钮")
        return self.assert_result()
