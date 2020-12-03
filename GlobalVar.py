import configparser
import logging
import os

projectName='consoleWorker'

root_dir = os.path.dirname(os.path.abspath(projectName))
if logging.root.isEnabledFor(logging.DEBUG):
     logging.debug('root_dir:%s' % root_dir)
# robot_dir = root_dir + "/pythonProject/consoleRobot/"
# if logging.root.isEnabledFor(logging.DEBUG):
#     logging.debug('robot_dir:%s' % robot_dir)
cf = configparser.RawConfigParser()
cf.read("worker.conf")
ErrorLogger = 'errorLogger'


# def init():
#     global config
#     config = {}
#
#
# def set(key, value):
#     config[key] = value
#
#
# def get(key):
#     return config[key]
