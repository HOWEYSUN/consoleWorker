# ke.com百科爬虫
# coding=UTF-8
import csv
import importlib
import logging
import logging.config
import queue

import threading
import re, time

import GlobalVar
from BasicRobot import BasicRobot
from webWorker.baobei.baobeiModel import Customer, BuildingProject, Report


class WorkShop():
    def __init__(self):
        self.doneItems = []

    def addDoneItem(self, itemNo):
        # 当队列满时按设置移除之前的单号
        if len(self.doneItems) > GlobalVar.cf.getint('itemQueue', 'maxQueue'):
            # 移除队列前部的指定数量的单号
            self.doneItems = self.doneItems[GlobalVar.cf.getint('itemQueue', 'popNum'):]
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
        report = Report(itemNo)

        userId = excel_data[1]
        userName = excel_data[2]
        tel = excel_data[3]
        sex = excel_data[4]
        desc = excel_data[5]
        customer = Customer(userId, tel, userName, sex)
        customer.setDesc(desc)

        projectId = excel_data[6]
        projectName = excel_data[7]
        project = BuildingProject(projectId, projectName)

        report.setCustomer(customer)
        report.setProject(project)

        workerModuleName = GlobalVar.cf.get('api', itemNo)
        workerModuleObj = importlib.import_module('.' + workerModuleName,
                                                  GlobalVar.cf.get('worker', 'baobeiWorkerPackage'))
        workerObj = getattr(workerModuleObj, workerModuleName)
        worker = workerObj()
        worker.setReport(report)

        baobeiRobot = BasicRobot(worker)
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f"worker(%s) is on work" % baobeiRobot.getWorkerNo())
        baobeiRobot.doJob()
        time.sleep(10)
        baobeiRobot.close()

    def handleCvs(self, itemNo):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f"write itemNo(%s) into reportHandled..." % itemNo)
        out = open('reportHandled.csv', 'a', newline='', encoding='utf-8')
        # 设定写入模式
        csv_write = csv.writer(out)
        # 写入具体内容
        csv_write.writerow([itemNo, 'done'])
        out.close()

    def doTask(self, itemQueue):
        while 1:
            if itemQueue.empty():
                time.sleep(10)
            self.work(itemQueue.get())

    def controller(self, itemQueue):
        while 1:
            if itemQueue.empty():
                if logging.root.isEnabledFor(logging.DEBUG):
                    logging.debug(f"读取文件获取执行任务")
                with open('customer.csv', 'r', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    # header = next(csv_reader)  # 读取第一行每一列的标题
                    for excel_data in csv_reader:
                        itemNo = excel_data[0]
                        if workerShop.isDoneItem(itemNo):
                            continue
                        self.addDoneItem(itemNo)
                        itemQueue.put(excel_data)
                time.sleep(30)


def main():
    # 初始化日志配置
    logging.config.fileConfig('logging.conf')

    # create logger
    global logger
    logger = logging.getLogger('root')


if __name__ == '__main__':
    main()
    workerShop = WorkShop()
    itemQueue = queue.Queue()
    threads = []
    wokerThread = threading.Thread(name='workShop(controller)', target=WorkShop.controller,
                                   args=(workerShop, itemQueue,))
    wokerThread.start()

    workerNum = GlobalVar.cf.getint('worker', 'workerNum')
    # 按配置开起子线程
    for i in range(0, workerNum):
        t = threading.Thread(name='workShop(No%s_worker)' % i, target=WorkShop.doTask,
                             args=(workerShop, itemQueue,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
