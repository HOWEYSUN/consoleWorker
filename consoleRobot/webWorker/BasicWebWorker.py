# web类型的工人, 基类需要初始化浏览器
# 默认初始化谷歌浏览器，若需要使用其他浏览器则在子类中重写init方法
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import GlobalVar
from BasicWorker import BasicWorker


class BasicWebWorker(BasicWorker):
    def __init__(self, workerNo):
        super().__init__(workerNo)

        # 起始页面
        # 一般起始页都固定为登录页面（若需要登录才可操作的）
        self.initUrl = ''
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
