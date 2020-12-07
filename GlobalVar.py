import configparser
import logging
import os
from prpcrypt import prpcrypt

projectName = 'pythonProject'

root_dir = os.path.dirname(os.path.abspath(projectName))
if logging.root.isEnabledFor(logging.DEBUG):
    logging.debug('root_dir:%s' % root_dir)
# robot_dir = root_dir + "/pythonProject/consoleRobot/"
# if logging.root.isEnabledFor(logging.DEBUG):
#     logging.debug('robot_dir:%s' % robot_dir)
cf = configparser.RawConfigParser()
cf.read("worker.conf")
ErrorLogger = 'errorLogger'
pc = prpcrypt(cf.get('project', 'robotKey'))


def decrypt(pText):
    return pc.decrypt(pText)


def encrypt(sText):
    return pc.encrypt(sText)
