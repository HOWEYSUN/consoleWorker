import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import GlobalVar


class BasicWorker:
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

    def close(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'worker(%s) 销毁!' % self.workerNo)
        pass

    def getWorkerNo(self):
        return self.workerNo

    # 自检
    # 需要爬取其他系统及网站的worker都应重写次方法，
    # 目的是给定时巡检程序判断该工人是否可用，若不可用应及时修正
    def check(self):
        return True

    # 参数检验
    def Validated(self):
        return True

    """
所有具体的实现类都必须重写此方法
    """
    def do(self):
        pass


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

        chrome_options.add_argument(GlobalVar.cf.get("setting", "userAgent"))
        if GlobalVar.cf.get("setting", "executablePath"):
            self.driver = webdriver.Chrome(options=chrome_options,
                                           executable_path=GlobalVar.cf.get("setting", "executablePath"))
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


class BaobeiWorker(BasicWebWorker):
    """
        报备类型的工人, 基类增加了报备单的设置（setReport）和登录页做为入口，以及退出页的跳转
    """

    def __init__(self, workerNo, loginUrl, logoutUrl):
        super().__init__(workerNo)
        self.initUrl = loginUrl
        self.endUrl = logoutUrl

    # 进入登录页
    def doLogin(self):
        self.driver.get(self.initUrl)

    def close(self):
        self.driver.get(self.endUrl)
        super().close()

    def setReport(self, report):
        self.report = report
