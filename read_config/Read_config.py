import configparser


def readconfig(path, section, option):
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8')
    conf_ = conf.get(section, option)
    return conf_
