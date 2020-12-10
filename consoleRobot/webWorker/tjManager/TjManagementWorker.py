import logging
import threading
import time
from GlobalVar import cf, decrypt
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from BasicWorker import BasicWebWorker


class TjManagementWorker(BasicWebWorker):
    """
        tujia系统同步员，工号WF01140001，属于住我房的第一个员工
        主要处理tujia PC端后台系统的同步工作
    """

    def __init__(self):
        # 01集团
        # 14住我房
        # 0001自增编号
        super().__init__('WF01140001')

    """
    重写浏览器初始化方法，使用已打开的浏览器来操作
    """
    def initWebdrive(self):
        self.loginFlag = False
        self.initUrl = 'https://passport.tujia.com/PortalSite/LoginPage/'
        # todo =========写死的谷歌浏览器配置，后续应做成配置化============
        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
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

    def doLogin(self, element):
        try:
            # super().doLogin()
            # 进入登录页
            # slideblock = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="nc_1_n1z"]'))
            # 鼠标点击滑动块不松开
            ActionChains(self.driver).click_and_hold(element).perform()
            # 将圆球滑至相对起点位置的 右边xx
            ActionChains(self.driver).move_by_offset(xoffset=50, yoffset=0).perform()
            time.sleep(0.1)
            ActionChains(self.driver).move_by_offset(xoffset=260, yoffset=0).perform()
            time.sleep(0.2)
            # 放开滑动块
            ActionChains(self.driver).release(element).perform()
            time.sleep(0.3)

            self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[1]/input').send_keys(
                decrypt(cf.get('worker', 'tj.userName')))
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[2]/input').send_keys(
                decrypt(cf.get('worker', 'tj.pwd')))
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/button').click()
            self.loginFlag = True
            self.writeLog(self.workerNo, '登录成功')
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'doLogin function')
            return False
        except Exception as e:
            self.logErrorMess(e, 'doLogin function')
            return False

        return True

    def switchTab(self):
        windows = self.driver.window_handles  # 获取所有的句柄
        # 我们要切换到 某一个标签页 就要知道 此标签页的 句柄
        self.driver.switch_to.window(windows[1])

    def close(self):
        if self.loginFlag:
            self.driver.get('https://passport.tujia.com/Landlord/Logout')
        super().close()