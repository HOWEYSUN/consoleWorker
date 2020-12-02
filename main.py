import time
import logging
import logging.config
from BasicRobot import BasicRobot
from webWorker.TjManagementWorker import TjManagementWorker
from webWorker.baobei.baobeiModel import Customer, BuildingProject
from webWorker.baobei.YajubaoWorker import YajubaoWorker


def main():
    # 初始化日志配置
    logging.config.fileConfig('logging.conf')

    # create logger
    global logger
    logger = logging.getLogger('root')


if __name__ == '__main__':
    main()
    worker = YajubaoWorker()
    customer = Customer(1001, '13518833380', '张女士', 0)
    customer.setDesc("倾向于三房两厅南北通透户型")
    project = BuildingProject(1001, '金沙湾')
    customer.addIntentions(project)
    worker.setCustomer(customer)
    baobeiRobot = BasicRobot(worker)
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(f"worker(%s) is on work" % baobeiRobot.getWorkerNo())
    baobeiRobot.doJob()

    time.sleep(15)
    baobeiRobot.close()
