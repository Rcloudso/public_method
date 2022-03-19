# 阿宋的Python学习之路
# 浏览器配置
from selenium import webdriver

'''
    浏览器配置类
'''


class OptionsChrome:
    def cache_option_chrome(self):
        options = webdriver.ChromeOptions()
        # 启动时默认最大化
        options.add_argument('start-maximized')
        # 有缓存的浏览器
        options.add_argument(r"--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default")
        # 去掉账号保存弹窗
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enable"] = False
        options.add_experimental_option('prefs', prefs)
        return options

    def options_chrome(self):
        """
        一般情况下使用这个函数即可，为一般网页形态
        :return:
        """
        options = webdriver.ChromeOptions()
        # 启动时默认最大化
        options.add_argument('start-maximized')

        # 无头模式
        # options.add_argument('--headless')

        # 设置尺寸大小
        # options.add_argument('window_size = 1920,1080')

        # 去掉浏览器自动化软件提示横条
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 有缓存的浏览器
        # options.add_argument(r"--user-data-dir=C:\Users\Worker\AppData\Local\Google\Chrome\User Data\Default")

        # 去掉账号保存弹窗
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enable"] = False
        options.add_experimental_option('prefs', prefs)

        # 无痕模式
        # options.add_argument('incognito')

        # 指定窗口打开位置
        # options.add_argument('window-position = 200,50')

        return options

    def options_phone(self):
        """
        需要手机样式的网页调用此函数
        :return:
        """
        options = webdriver.ChromeOptions()

        # 手机模式
        mobile_emulation = {"deviceName": "iPhone X"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        # 有缓存的浏览器
        options.add_argument(r"--user-data-dir=C:\Users\Worker\AppData\Local\Google\Chrome\User Data\Default")

        # 去掉账号保存弹窗
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enable"] = False
        options.add_experimental_option('prefs', prefs)

        return options
