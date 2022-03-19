# 阿宋的Python学习之路
"""
    测试套件TestSuite
        物理形态可以理解为文件夹
        套件基于运行器运行
        测试套件添加测试用例的方法：
            1.单独添加测试用例
            2.将测试用例作为一个列表进行传入
            3.添加一整个类作为用例
            4.通过文件名称添加用例
                4.1.基于第4种方式，将文件名称作为列表传入
            5.批量添加测试用例：
                (1)定义测试用例获取途径
                (2)使用变量获取套件对象
                (3)运行时传参为套件对象
"""
import os
import time
import unittest
from HTMLTestReportCN import HTMLTestRunner


def one_case(testcase, level=2):
    # 第一种添加方式：添加单个测试用例
    suite = unittest.TestSuite()
    suite.addTest(testcase)
    runner = unittest.TextTestRunner(verbosity=level)
    runner.run(suite)


def list_cases(test_cases_list, level=2):
    # 第二种添加方式：将测试用例作为一个列表进行传入
    suite = unittest.TestSuite()
    try:
        suite.addTests(test_cases_list)
        runner = unittest.TextTestRunner(verbosity=level)
        runner.run(suite)
    except Exception as e:
        print("请传入一个列表作为参数！")
        print("*" * 20)
        print(e)


def class_cases(class_name, level):
    # 第三种添加方式：添加一整个类作为用例
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(class_name))
    runner = unittest.TextTestRunner(verbosity=level)
    runner.run(suite)


def file_cases(file_name, level):
    # 第四种添加方式：通过文件名称添加用例
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromName(file_name))
    runner = unittest.TextTestRunner(verbosity=level)
    runner.run(suite)


def list_file_cases(file_name_list, level):
    # 第4.1种添加方式：将测试用例文件作为一个列表进行传入
    suite = unittest.TestSuite()
    try:
        suite.addTests(unittest.TestLoader().loadTestsFromNames(file_name_list))
        runner = unittest.TextTestRunner(verbosity=level)
        runner.run(suite)
    except Exception as e:
        print("请传入一个列表作为参数！")
        print("*" * 20)
        print(e)


# 第5种添加方式：从一个文件夹中导入测试用例的py文件
def file_cases_html_report_run(path, report_tester, report_title, report_description, report_dir):
    """
        配置HTMLTestRunner的测试报告信息:
            测试执行者：在HTMLTestReport报告中专属参数
            report_tester = '阿宋'
            保存路径:
            report_dir = '../report/'
            测试报告的title:
            report_title = '阿宋的测试报告'
            描述:
            report_description = '这是测试报告的描述'
    """
    discover = unittest.defaultTestLoader.discover(start_dir=path, pattern='test*.py')
    t = time.strftime('%Y-%m-%d_%H-%M-%S')
    # 测试报告文件，需要指定路径，加上文件名称
    report_file = report_dir + t + 'reportCN.html'

    # 生成路径
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)

    # 生成HTMLTestRunner测试报告，本质意义上就是写入一个文件
    with open(report_file, 'wb') as file:
        runner = HTMLTestRunner(stream=file, title=report_title,
                                description=report_description, verbosity=2,
                                tester=report_tester)
        runner.run(discover)
