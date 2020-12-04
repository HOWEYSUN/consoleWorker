import csv
import logging
import logging.config
from GlobalVar import root_dir
from flask import request, Flask


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
