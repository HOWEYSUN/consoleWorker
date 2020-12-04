import csv
import logging
import logging.config
from GlobalVar import root_dir
from flask import request, Flask
from multiprocessing import Process

from workshop import initWorkShop

app = Flask(__name__)
app.debug = True


def main():
    # 初始化日志配置
    logging.config.fileConfig('logging.conf')

    # create logger
    global logger
    logger = logging.getLogger('root')


@app.route('/<itemNo>')
def baobei(itemNo):
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(f"baobei api接受了一个请求")
    channelNo = request.args.get('channelNo', '')
    userId = request.args.get('userId', '')
    userName = request.args.get('userName', '')
    tel = request.args.get('tel', '')
    sex = request.args.get('sex', '')
    desc = request.args.get('desc', '')
    projectId = request.args.get('projectId', '')
    projectName = request.args.get('projectName', '')

    if userId:
        # 打开文件，追加a
        out = open('customer.csv', 'a', newline='', encoding='utf-8')
        # 设定写入模式
        csv_write = csv.writer(out)
        # 写入具体内容
        csv_write.writerow([itemNo, channelNo, userId, userName, tel, sex, desc, projectId, projectName])
        out.close()

    return '接收成功!'


if __name__ == '__main__':
    main()
    if logging.root.isEnabledFor(logging.DEBUG):
        logger.debug(root_dir)
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
#  http://127.0.0.1:5000/1001234?userId=1002&tel=13646585588&userName=陈先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾
#  http://127.0.0.1:5000/1001235?userId=1003&tel=13788888888&userName=王先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001236?userId=1004&tel=13888888888&userName=黄先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾
#  http://127.0.0.1:5000/1001237?userId=1005&tel=13988888888&userName=林先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾
#  http://127.0.0.1:5000/1001238?userId=1006&tel=13699999999&userName=苏先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001239?userId=1007&tel=15992428649&userName=罗先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾
#  http://127.0.0.1:5000/1001240?userId=1008&tel=13518833380&userName=方先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001243?userId=1009&tel=13485201258&userName=尉先生&sex=1&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾
#  http://127.0.0.1:5000/1001244?userId=1010&tel=13976536485&userName=黄女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001245?userId=1011&tel=18876733310&userName=陈女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾
#  http://127.0.0.1:5000/1001246?userId=1012&tel=13485201258&userName=罗女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾
#  http://127.0.0.1:5000/1001247?userId=1013&tel=18289552238&userName=苏女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001248?userId=1014&tel=15008925299&userName=王女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1002&projectName=清水湾
#  http://127.0.0.1:5000/1001249?userId=1015&tel=13976536485&userName=钱女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1003&projectName=星光城
#  http://127.0.0.1:5000/1001250?userId=1016&tel=13800138000&userName=林女士&sex=0&desc=倾向于三房两厅南北通透户型&projectId=1001&projectName=金沙湾