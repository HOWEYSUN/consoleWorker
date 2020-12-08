import csv
import logging
import logging.config
from flask import request, Flask

app = Flask(__name__)
app.debug = True


@app.route('/<itemNo>')
def baobei(itemNo):
    if logging.root.isEnabledFor(logging.DEBUG):
        logging.debug(f"baobei api接受了一个请求")
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
        out = open('export/customer.csv', 'a', newline='', encoding='utf-8')
        # 设定写入模式
        csv_write = csv.writer(out)
        # 写入具体内容
        csv_write.writerow([itemNo, channelNo, userId, userName, tel, sex, desc, projectId, projectName])
        out.close()

    return '接收成功!'


if __name__ == '__main__':
    app.run()
