from selenium import webdriver
from My_option.Chrome_Options import OptionsChrome


def all_driver(text):
    if text == 'Chrome':
        browser_driver = webdriver.Chrome(options=OptionsChrome().options_chrome())
    else:
        try:
            browser_driver = getattr(webdriver, text)()
        except Exception as e:
            print(e)
            browser_driver = webdriver.Chrome(options=OptionsChrome().options_chrome())
    return browser_driver


def chrome_phone_driver():
    browser_driver = webdriver.Chrome(options=OptionsChrome().options_phone())
    return browser_driver


def chrome_driver():
    browser_driver = webdriver.Chrome(options=OptionsChrome().options_chrome())
    return browser_driver


def cache_chrome_driver():
    browser_driver = webdriver.Chrome(options=OptionsChrome().cache_option_chrome())
    return browser_driver
