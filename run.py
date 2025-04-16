"""
测试框架主入口
支持多种运行方式和参数配置
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="UI自动化测试框架")
    
    # 测试选项
    parser.add_argument("--tests", "-t", type=str, default="tests",
                        help="测试目录或文件路径")
    parser.add_argument("--markers", "-m", type=str, default=None,
                        help="仅运行标记的测试，例如 'smoke or regression'")
    
    # 浏览器选项
    parser.add_argument("--browser", "-b", type=str, default="chrome",
                        help="浏览器类型: chrome, firefox, edge")
    parser.add_argument("--headless", action="store_true",
                        help="启用无头模式")
    parser.add_argument("--mobile", action="store_true",
                        help="启用移动设备模拟")
    
    # 环境选项
    parser.add_argument("--env", "-e", type=str, default="test",
                        help="测试环境: dev, test, stage, prod")
    
    # 并行选项
    parser.add_argument("--workers", "-w", type=int, default=0,
                        help="并行执行的工作进程数，0表示不并行")
    
    # 重试选项
    parser.add_argument("--rerun", "-r", type=int, default=0,
                        help="失败重试次数")
    
    # 报告选项
    parser.add_argument("--html-report", action="store_true",
                        help="生成HTML报告")
    parser.add_argument("--report-title", type=str, default="UI自动化测试报告",
                        help="HTML报告标题")
    
    return parser.parse_args()


def run_tests(args):
    """运行测试"""
    # 构建pytest命令
    pytest_args = ["-v", args.tests]
    
    # 添加标记
    if args.markers:
        pytest_args.extend(["-m", args.markers])
    
    # 添加浏览器参数
    pytest_args.extend(["--browser", args.browser])
    
    if args.headless:
        pytest_args.append("--headless")
    
    if args.mobile:
        pytest_args.append("--mobile")
    
    # 添加环境参数
    pytest_args.extend(["--env", args.env])
    
    # 添加并行选项
    if args.workers > 0:
        pytest_args.extend(["-n", str(args.workers)])
    
    # 添加重试选项
    if args.rerun > 0:
        pytest_args.extend(["--reruns", str(args.rerun)])
    
    # 添加HTML报告选项
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        
        report_path = report_dir / f"report_{timestamp}.html"
        pytest_args.extend([
            "--html", str(report_path),
            "--self-contained-html",
        ])
    
    # 打印执行命令
    cmd_str = "pytest " + " ".join(pytest_args)
    print(f"执行命令: {cmd_str}")
    
    # 运行pytest
    return subprocess.call(["pytest"] + pytest_args)


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置环境变量
    os.environ["BROWSER_TYPE"] = args.browser
    os.environ["HEADLESS"] = str(args.headless).lower()
    
    # 运行测试
    exit_code = run_tests(args)
    
    # 退出
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 