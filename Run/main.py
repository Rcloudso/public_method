# 框架主入口，从此处直接运行即可
import unittest
from unittestreport import TestRunner
from test_cases_debug import test_0_success_login
from test_cases_debug import test_1_0_add_shop

from testsuite.test_suite import file_cases_html_report_run

if __name__ == '__main__':
    # report = file_cases_html_report_run(path='./test_cases_debug',
    #                                     report_tester='阿宋',
    #                                     report_dir='./report/',
    #                                     report_title='自动化测试报告',
    #                                     report_description="Niushop商城的自动化测试报告")

    # 测试套件
    # suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_0_success_login.TestLogin)
    suite = unittest.defaultTestLoader.discover("./test_cases_debug")
    # 创建执行对象
    runner = TestRunner(title="自动化测试报告", tester="阿宋", desc="Niushop商城的自动化测试报告", suite=suite)
    # 执行测试用例，失败重运行设置为3次，间隔时间为2秒
    runner.rerun_run(count=3, interval=2)
