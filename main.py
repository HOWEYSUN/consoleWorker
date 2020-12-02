import time

from basicRobot import BasicRobot
from worker.TjManagementWorker import TjManagementWorker


managerWorker = TjManagementWorker()
basicRobot = BasicRobot(managerWorker)
basicRobot.doJob()

time.sleep(5)
basicRobot.close()

