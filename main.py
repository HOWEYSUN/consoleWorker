import time
import logging
import logging.config
from BasicRobot import BasicRobot
from GlobalVar import robot_dir
from webWorker.TjManagementWorker import TjManagementWorker
from webWorker.baobei.baobeiModel import Customer, BuildingProject
from webWorker.baobei.YajubaoWorker import YajubaoWorker
from flask import request, Flask
import GlobalVar
import importlib
from BasicRobot import BasicRobot
from webWorker.baobei.baobeiModel import Customer, BuildingProject

app = Flask(__name__)
app.debug = True

def main():
    # 初始化日志配置
    logging.config.fileConfig('logging.conf')

    # create logger
    global logger
    logger = logging.getLogger('root')


@app.route('/<channelId>')
def baobei(channelId):
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(f"baobei api接受一个(%s)请求" % channelId)
    userId = request.args.get('userId', '')
    userName = request.args.get('userName', '')
    tel = request.args.get('tel', '')
    sex = request.args.get('sex', '')
    desc = request.args.get('desc', '')
    projectId = request.args.get('projectId', '')
    projectName = request.args.get('projectName', '')
    customer = Customer(userId, tel, userName, sex)
    customer.setDesc(desc)

    project = BuildingProject(projectId, projectName)
    customer.addIntentions(project)

    workerModuleName = GlobalVar.cf.get('api', channelId)
    workerModuleObj = importlib.import_module(workerModuleName, 'webWorker.baobei')
    workerObj = getattr(workerModuleObj, workerModuleName)
    worker = workerObj()
    worker.setCustomer(customer)
    baobeiRobot = BasicRobot(worker)
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(f"worker(%s) is on work" % baobeiRobot.getWorkerNo())
    baobeiRobot.doJob()

    time.sleep(10)
    baobeiRobot.close()

    return 'success!'


if __name__ == '__main__':
    main()
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(robot_dir)
    app.run()

# def woker():
#     worker = YajubaoWorker()
#     customer = Customer(1001, '13518833380', '张女士', 0)
#     customer.setDesc("倾向于三房两厅南北通透户型")
#     project = BuildingProject(1001, '金沙湾')
#     customer.addIntentions(project)
#     worker.setCustomer(customer)
#     baobeiRobot = BasicRobot(worker)
#     if logging.root.isEnabledFor(logging.DEBUG):
#         logger.debug(f"worker(%s) is on work" % baobeiRobot.getWorkerNo())
#     baobeiRobot.doJob()
#
#     time.sleep(10)
#     baobeiRobot.close()
#  http://127.0.0.1:5000/1001233?userId=1001&tel=13518833380&userName=张女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾


