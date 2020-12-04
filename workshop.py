# coding=UTF-8
import csv
import importlib
import logging
import logging.config
import queue

import threading
import time
import traceback

import GlobalVar
from BasicRobot import BasicRobot
from webWorker.baobei.baobeiModel import Customer, BuildingProject, Report


class WorkShop:
    """工作间类
       主要使用的是controller、daTask两个方法，主持多线程操作
       初始化需要指定员工类的全路径名（如报备类工作间为：baobeiWorkerPackage）
    """

    def __init__(self, workerPackage):
        self.workerPackage = workerPackage
        self.doneItems = []

    def addDoneItem(self, itemNo):
        # 当队列满时按设置移除之前的单号
        if len(self.doneItems) > GlobalVar.cf.getint('workShop', 'maxQueue'):
            # 移除队列前部的指定数量的单号
            self.doneItems = self.doneItems[GlobalVar.cf.getint('workShop', 'popNum'):]
        self.doneItems.append(itemNo)
        self.handleCvs(itemNo)
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'doneItems(%s)' % self.doneItems)

    def isDoneItem(self, itemNo):
        return itemNo in self.doneItems

    def work(self, excel_data):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f"workItem[%s] is on process" % excel_data)

        itemNo = excel_data[0]
        channelNo = excel_data[1]
        report = Report(itemNo, channelNo)

        userId = excel_data[2]
        userName = excel_data[3]
        tel = excel_data[4]
        sex = excel_data[5]
        desc = excel_data[6]
        customer = Customer(userId, tel, userName, sex)
        customer.setDesc(desc)

        projectId = excel_data[7]
        projectName = excel_data[8]
        project = BuildingProject(projectId, projectName)

        report.setCustomer(customer)
        report.setProject(project)

        #根据渠道ID来获取配置中指定的员工类
        workerModuleName = GlobalVar.cf.get('api', channelNo)
        workerModuleObj = importlib.import_module('.' + workerModuleName, self.workerPackage)
        workerObj = getattr(workerModuleObj, workerModuleName)
        worker = workerObj()
        worker.setReport(report)

        robot = BasicRobot(worker)
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug("worker({0}) is process the report({1})".format(robot.getWorkerNo(), itemNo))
        try:
            robot.doJob()
            self.handleCvs(itemNo, 'done')
        except Exception as e:
            logging.error("worker({0}) handle report({1}) failed".format(robot.getWorkerNo(), itemNo))
            logging.error("error mess:%s" % traceback.format_exc())
            self.handleCvs(itemNo, 'failed')

        time.sleep(2)
        robot.close()


    def handleCvs(self, itemNo, workerStatue='working'):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f"write itemNo(%s) into reportHandled..." % itemNo)
        out = open('reportHandled.csv', 'a', newline='', encoding='utf-8')
        # 设定写入模式
        csv_write = csv.writer(out)
        # 写入具体内容
        csv_write.writerow([itemNo, workerStatue])
        out.close()

    def doTask(self, itemQueue):
        """
        工作台方法（消费者），工作者从此处获得操作单来进行work操作
        :param itemQueue: 操作单队列
        :return: None
        """
        while 1:
            if itemQueue.empty():
                time.sleep(10)
            self.work(itemQueue.get())#若队列中有待处理的单则取出处理

    def controller(self, itemQueue):
        """
        监工方法（生产者），负责获得操作单并放入操作单队列
        :param itemQueue: 操作单队列
        :return: None
        """
        while 1:
            if itemQueue.empty():
                if logging.root.isEnabledFor(logging.DEBUG):
                    logging.debug(f"读取文件获取执行任务")
                # todo 这里取操作单的操作应从数据库中获取
                with open('customer.csv', 'r', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for excel_data in csv_reader:
                        if len(excel_data)<=0:
                            continue
                        itemNo = excel_data[0]
                        if self.isDoneItem(itemNo):#判断该单据是否处理过
                            continue
                        self.addDoneItem(itemNo)#将需要处理的单号置为已处理 #todo 这里需要考虑操作失败时的策略
                        itemQueue.put(excel_data)#将需要处理的单号丢进队列里
                time.sleep(30)


def initWorkShop(workerNum=0):
    """
    初始化工作间
    :param workerNum: 操作单队列
    :return: None
    """
    # 初始化日志配置
    logging.config.fileConfig('logging.conf')

    # create logger
    global logger
    logger = logging.getLogger('root')

    workerShop = WorkShop(GlobalVar.cf.get('workShop', 'baobeiWorkerPackage'))
    itemQueue = queue.Queue()
    threads = []
    wokerThread = threading.Thread(name='workShop(controller)', target=WorkShop.controller,
                                   args=(workerShop, itemQueue,))
    wokerThread.start()
    if workerNum <= 0 :#若初始化工作者人数为负数或为空则从配置中获得
        workerNum = GlobalVar.cf.getint('workShop', 'workerNum')

    # 按配置开起子线程
    for i in range(0, workerNum):
        t = threading.Thread(name='workShop(No%s_worker)' % i, target=WorkShop.doTask,
                             args=(workerShop, itemQueue,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':
    initWorkShop()
