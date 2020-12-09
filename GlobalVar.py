import configparser
import logging
from logging import config
from os import path

from beanBuilder.ProjectBeanBuilder import ProjectBeanBuilder
from util.prpcrypt import prpcrypt

localProjectName = 'pythonProject'
root_path = path.join(path.dirname(__file__).split(localProjectName)[0])
project_path = path.join(root_path, localProjectName)
logConf_file_path = path.join(root_path, localProjectName+'/conf/logging.conf')
projectConf_file_path = path.join(root_path, localProjectName+'/conf/worker.conf')
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
beanBuilder = ProjectBeanBuilder()
beanBuilder.initBeans()


def decrypt(pText):
    return pc.decrypt(pText)


def encrypt(sText):
    return pc.encrypt(sText)
