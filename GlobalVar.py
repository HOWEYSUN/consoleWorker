import configparser
import logging
from os import path
from util.prpcrypt import prpcrypt

localProjectName = 'pythonProject'
logConf_file_path = path.join(path.dirname(path.abspath(localProjectName)), 'conf/logging.conf')
projectConf_file_path = path.join(path.dirname(path.abspath(localProjectName)), 'conf/worker.conf')

# 初始化日志配置
logging.config.fileConfig(logConf_file_path)

if logging.root.isEnabledFor(logging.DEBUG):
    logging.debug('log configure file:%s' % logConf_file_path)
    logging.debug('project configure file:%s' % projectConf_file_path)

# 读取项目配置文件
cf = configparser.RawConfigParser()
cf.read(projectConf_file_path)

# 初始化加密类实例
pc = prpcrypt(cf.get('project', 'robotKey'))


def decrypt(pText):
    return pc.decrypt(pText)


def encrypt(sText):
    return pc.encrypt(sText)
