import logging

'''
    log配置函数
'''


def log():
    # fmt = '%(asctime)s %(funcName)s %(name)s %(filename)s %(message)s'
    # logging.basicConfig(level=logging.INFO, format=fmt, filename='log.txt')
    # return logging

    # 设置控制台打印的颜色
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'black',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    # 创建日志器
    logger = logging.getLogger('Log')

    # 判断是否存在handlers
    if not logger.handlers:
        logger.setLevel(level=logging.INFO)

        # 创建控制台处理器
        sh = logging.StreamHandler()
        logger.addHandler(sh)

        # 创建文件处理器
        # fh = logging.FileHandler('../log/log.txt', encoding='utf-8')
        # logger.addHandler(fh)

        # 创建格式处理器
        fmt_sh = '%(asctime)s %(funcName)s %(name)s %(filename)s %(message)s'
        format_stream = logging.Formatter(fmt_sh)

        # fmt_fh = '%(asctime)s %(funcName)s %(message)s'
        # format_file = logging.Formatter(fmt_fh)

        # 给控制台log添加格式处理器
        sh.setFormatter(format_stream)

        # 给文件log添加格式处理器
        # fh.setFormatter(format_file)

    # 如果不进行handlers的判断，可以使用清理handlers的方法
    # logger.handlers.clear()

    return logger
