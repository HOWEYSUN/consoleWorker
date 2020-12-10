import csv
import logging
import threading
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from GlobalVar import cf, beanBuilder, project_path
from beanBuilder.ProjectBeanBuilder import ProjectBeanBuilder


class BasicWorker(object):
    """
        所有类型的工人的基类，每一个分类的工人都应继承此基类
    """

    # 初始化需要定义工人的工号
    # 编码规则为：WFXXYYZZZZ
    # XX为集团编码01
    # YY为一级部门或子公司编码，具体对应编码参考部门编码，如客服中心04
    # ZZZZ为工人自增编号如一号工人：0001
    def __init__(self, workerNo):
        self.workerNo = workerNo
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'worker(%s) 初始化!' % workerNo)
        self.beanBuilder = ProjectBeanBuilder()

    def close(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'worker(%s) 工作结束!' % self.workerNo)
        pass

    def getWorkerNo(self):
        return self.workerNo

    def check(self):
        """
        # 自检
        # 需要爬取其他系统及网站的worker都应重写次方法，
        # 目的是给定时巡检程序判断该工人是否可用，若不可用应及时修正
        :return: 该工人是否检测通过
        """
        return True

    # 参数检验
    def Validated(self):
        """
        校验传给工人的参数是否正确
        :return: 参数校验是否通过
        """
        return True

    def doBySop(self):
        """
            所有具体的实现类都必须重写此方法
        :return: 工作结果
        """
        pass

    # todo 需要调整为DB存储
    def writeLog(self, itemNo, execLog, logLevel='debug'):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug("logLevel({0}) - itemNo({1}) execute mess:{2}".format(logLevel, itemNo, execLog))

        # 是否配置将日志写入文件
        if cf.get("worker", "isSaveExecLog")\
                or logLevel == 'error':
            out = open(project_path + '/export/executeLog.csv', 'a', newline='', encoding='utf-8')
            # 设定写入模式
            csv_write = csv.writer(out)
            # 写入具体内容
            csv_write.writerow([itemNo, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), execLog])
            out.close()

    def handleCvs(self, itemNo, workerStatue='working'):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f"write itemNo(%s)'s logs into cvs..." % itemNo)
        self.writeLog(itemNo, workerStatue)
        # if logging.root.isEnabledFor(logging.DEBUG):
        #     logging.debug(f"write itemNo(%s) into reportHandled..." % itemNo)
        # out = open('reportHandled.csv', 'a', newline='', encoding='utf-8')
        # # 设定写入模式
        # csv_write = csv.writer(out)
        # # 写入具体内容
        # csv_write.writerow([itemNo, workerStatue])
        # out.close()


class BasicWebWorker(BasicWorker):
    """
        web类型的工人, 基类需要初始化浏览器
        默认初始化谷歌浏览器，若需要使用其他浏览器则在子类中重写init方法
    """

    def __init__(self, workerNo):
        super().__init__(workerNo)

        # 起始页面
        # 一般起始页都固定为登录页面（若需要登录才可操作的）
        self.initUrl = ''
        self.initWebdrive()

    def initWebdrive(self):
        # todo =========写死的谷歌浏览器配置，后续应做成配置化============
        chrome_options = Options()
        # 去除浏览器自动测试软件的提示
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

        chrome_options.add_argument(cf.get("workShop", "userAgent"))
        if cf.get("workShop", "executablePath"):
            self.driver = webdriver.Chrome(options=chrome_options,
                                           executable_path=cf.get("workShop", "executablePath"))
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        # 简单地避免反爬虫对navigator的检验
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 谷歌浏览器初始化完成！' % self.workerNo)
        # end todo =========写死的谷歌浏览器配置，后续应做成配置化============

    # 进入登录页
    def doLogin(self):
        self.driver.get(self.initUrl)

    def close(self):
        self.driver.quit()
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 谷歌浏览器关闭完成！' % self.workerNo)
        super().close()

    # 检查对应的页面元素是否存在
    def checkElement(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def logErrorMess(self, e, where):
        mess = 'worker({0}) work occur:{1} on ({2})！'.format(self.workerNo, str(e), where)
        logging.error(mess)
        logging.error("error mess:%s" % traceback.format_exc())
        self.writeLog(self.workerNo, mess, 'error')

    def saveScreenshot(self, screenName=None):
        """
        截图保存
        :param screenName: 截图文件名，默认设置为当前workerNo.png
        :return:
        """
        if screenName == None:
            screenName = project_path + '/export/%s.png' % self.workerNo
        self.driver.save_screenshot(screenName)

    def doBySop(self):
        workerBean = beanBuilder.getBeanByWorkerNo(self.workerNo)



class ReportWorker(BasicWebWorker):
    """
        报备类型的工人, 基类增加了报备单的设置（setReport）和登录页做为入口，以及退出页的跳转
    """

    def __init__(self, workerNo, loginUrl, logoutUrl):
        super().__init__(workerNo)
        self.initUrl = loginUrl
        self.endUrl = logoutUrl

    def close(self):
        self.driver.get(self.endUrl)
        super().close()

    def setReport(self, report):
        self.report = report

    def logErrorMess(self, e, where):
        mess = 'worker({0}) work for report({1}) occur:{2} on ({3})！'.format(self.workerNo, self.report.reportNo, str(e), where)
        logging.error(mess)
        logging.error("error mess:%s" % traceback.format_exc())
        self.writeLog(self, self.report.reportNo, mess, 'error')