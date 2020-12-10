# utf-8
import importlib
from BasicRobot import BasicRobot
import GlobalVar
from webWorker.report.ReportModel import Report, BuildingProject, Customer


def main():

    # 先后台打开一个浏览器
    chromeDriver = 'C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe '
    args = '--remote-debugging-port=9222  --user-data-dir="E:/python-workspace/chrome/AutomationProfile"'
    # w = os.system(chromeDriver)

    # 然后调用途家worker(为了绕过途家的检测，无奈之举)
    # itemNo = '1001233'
    # channelNo = ''
    # report = Report(itemNo, channelNo)
    #
    # userId = 1
    # userName = '王先生'
    # tel = '13800138000'
    # sex = 1
    # desc = '备注信息:你好！'
    # customer = Customer(userId, tel, userName, sex)
    # customer.setDesc(desc)
    #
    # projectId = '10001'
    # projectName = '金沙湾'
    # project = BuildingProject(projectId, projectName)
    #
    # report.setCustomer(customer)
    # report.setProject(project)

    workerModuleName = 'YajubaoWorker'
    workerModuleObj = importlib.import_module('.' + workerModuleName, 'consoleRobot.webWorker.report')
    workerObj = getattr(workerModuleObj, workerModuleName)
    worker = workerObj()
    # worker.setReport(report)

    robot = BasicRobot(worker)
    robot.doJob()
    robot.close()


if __name__ == '__main__':
    main()
