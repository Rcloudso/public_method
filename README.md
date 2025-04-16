# UI自动化测试框架

这是一个基于Selenium和Pytest的UI自动化测试框架，采用页面对象模式(POM)设计，提供可靠、可维护和高效的Web UI自动化测试方案。

## 特性

- **多浏览器支持**: 支持Chrome、Firefox和Edge
- **自动驱动管理**: 使用webdriver-manager自动下载和管理浏览器驱动
- **页面对象模式**: 将页面UI元素和操作封装到页面对象中，使测试代码更加清晰和易于维护
- **灵活配置**: 支持多环境配置(开发、测试、预发布、生产)
- **丰富的命令行选项**: 灵活配置测试执行参数
- **高级日志**: 使用loguru提供更强大的日志功能
- **自动截图**: 测试失败时自动截图
- **HTML测试报告**: 生成美观的HTML测试报告
- **失败重试**: 支持失败用例自动重试
- **并行测试**: 支持多进程并行执行测试
- **数据安全**: 加密敏感数据的处理

## 安装

1. 克隆项目:

```bash
git clone https://github.com/yourusername/ui-automation-framework.git
cd ui-automation-framework
```

2. 安装依赖:

```bash
pip install -r requirements.txt
```

## 项目结构

```
ui-automation-framework/
├── base/                   # 基础组件
│   ├── browser_driver.py   # 浏览器驱动管理
│   ├── page.py             # 页面对象基类
│   ├── test_case.py        # 测试用例基类
│   └── __init__.py
├── config/                 # 配置文件
│   ├── dev.yaml            # 开发环境配置
│   ├── test.yaml           # 测试环境配置
│   └── __init__.py
├── pages/                  # 页面对象
│   ├── login_page.py       # 登录页面对象
│   └── __init__.py
├── tests/                  # 测试用例
│   ├── test_login.py       # 登录功能测试
│   └── __init__.py
├── utils/                  # 工具模块
│   ├── logger.py           # 日志工具
│   ├── config_reader.py    # 配置读取工具
│   ├── encryption.py       # 加密工具
│   └── __init__.py
├── conftest.py             # Pytest配置和夹具
├── pytest.ini              # Pytest配置
├── requirements.txt        # 项目依赖
├── run.py                  # 测试启动脚本
└── README.md               # 项目说明
```

## 使用方法

### 基本用法

运行所有测试:

```bash
python run.py
```

运行特定测试:

```bash
python run.py --tests tests/test_login.py
```

### 进阶用法

使用特定浏览器:

```bash
python run.py --browser firefox
```

无头模式:

```bash
python run.py --headless
```

运行特定标记的测试:

```bash
python run.py --markers "smoke or regression"
```

指定测试环境:

```bash
python run.py --env stage
```

并行执行:

```bash
python run.py --workers 4
```

失败重试:

```bash
python run.py --rerun 2
```

生成HTML报告:

```bash
python run.py --html-report
```

组合使用:

```bash
python run.py --browser chrome --headless --markers "smoke" --env test --workers 4 --rerun 1 --html-report
```

## 编写测试

### 页面对象

创建新的页面对象:

```python
from selenium.webdriver.common.by import By
from base.page import BasePage

class HomePage(BasePage):
    # 页面URL
    URL = "https://example.com/home"
    
    # 页面元素
    WELCOME_MESSAGE = (By.ID, "welcome")
    LOGOUT_BUTTON = (By.ID, "logout")
    
    def get_welcome_message(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def logout(self):
        self.click(self.LOGOUT_BUTTON)
        self.wait_for_page_load()
```

### 测试用例

创建新的测试用例:

```python
import pytest
from pages.home_page import HomePage

@pytest.mark.functional
class TestHomePage:
    def test_welcome_message(self, driver, config):
        # 创建页面对象
        home_page = HomePage(driver)
        
        # 获取欢迎消息
        message = home_page.get_welcome_message()
        
        # 验证
        assert "Welcome" in message, "欢迎消息不正确"
```

## 贡献

欢迎贡献代码、报告问题或提出改进建议。请随时提交Pull Request或创建Issue。

## 许可证

MIT 