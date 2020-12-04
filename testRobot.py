# utf-8
import importlib
import win32api
from BasicRobot import BasicRobot


def main():
    # 先后台打开一个浏览器
    chromeDriver = 'C:/Users/Administrator/AppData/Local/Google/Chrome/Application/chrome.exe '
    args = '--remote-debugging-port=9222  --user-data-dir="E:/python-workspace/chrome/AutomationProfile"'
    # w = os.system(chromeDriver)
    win32api.ShellExecute(0, 'open', chromeDriver, args, '', 0)

    # 然后调用途家worker(为了绕过途家的检测，无奈之举)
    workerModuleName = 'TjManagementWorker'
    workerModuleObj = importlib.import_module('.' + workerModuleName, 'consoleRobot.webWorker')
    workerObj = getattr(workerModuleObj, workerModuleName)
    worker = workerObj()

    robot = BasicRobot(worker)
    robot.doJob()
    robot.close()


if __name__ == '__main__':
    main()
