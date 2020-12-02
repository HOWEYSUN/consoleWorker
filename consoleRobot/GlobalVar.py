import configparser
import logging
import os

root_dir = os.path.dirname(os.path.abspath('.'))
if logging.root.isEnabledFor(logging.DEBUG):
    logging.debug('root_dir:%s' % root_dir)
robot_dir = root_dir + "/consoleWorker/consoleRobot/"
if logging.root.isEnabledFor(logging.DEBUG):
    logging.debug('robot_dir:%s' % robot_dir)
cf = configparser.RawConfigParser()
cf.read(robot_dir + "worker.conf")
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
