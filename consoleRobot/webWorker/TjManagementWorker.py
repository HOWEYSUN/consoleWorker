import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import GlobalVar
from BasicWorker import BasicWebWorker


class TjManagementWorker(BasicWebWorker):
    def __init__(self):
        # 01集团
        # 18住我房
        # 03自增编号
        super().__init__('WF0118001')
        self.initUrl = 'https://passport.tujia.com/PortalSite/LoginPage/'
        self.loginFlag = False

    """
    重写浏览器初始化方法，使用已打开的浏览器来操作
    """
    def initWebdrive(self):
        # todo =========写死的谷歌浏览器配置，后续应做成配置化============
        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # 去除浏览器自动测试软件的提示
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

        chrome_options.add_argument(GlobalVar.cf.get("workShop", "userAgent"))
        if GlobalVar.cf.get("workShop", "executablePath"):
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

    def doLogin(self):
        try:
            super().doLogin()
            # 进入登录页
            slideblock = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="nc_1_n1z"]'))
            # 鼠标点击滑动块不松开
            ActionChains(self.driver).click_and_hold(slideblock).perform()
            # 将圆球滑至相对起点位置的 右边xx
            ActionChains(self.driver).move_by_offset(xoffset=50, yoffset=0).perform()
            time.sleep(0.1)
            ActionChains(self.driver).move_by_offset(xoffset=260, yoffset=0).perform()
            time.sleep(0.2)
            # 放开滑动块
            ActionChains(self.driver).release(slideblock).perform()
            time.sleep(0.3)

            self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[1]/input').send_keys(
                GlobalVar.decrypt(GlobalVar.cf.get('workShop', 'tj.userName')))
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[2]/input').send_keys(
                GlobalVar.decrypt(GlobalVar.cf.get('workShop', 'tj.pwd')))
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

    def do(self):
        if not self.doLogin():
            self.writeLog(self.workerNo, '登录失败！')
            return False

        # 进入业主后台
        WebDriverWait(self.driver, 10)\
            .until(lambda x: x.find_element_by_xpath('//*[@id="app"]/section/div/div[2]/div/div[2]/div[2]/a')).click()
        self.writeLog(self.workerNo, '登录成功！')

        windows = self.driver.window_handles  # 获取所有的句柄
        # 我们要切换到 某一个标签页 就要知道 此标签页的 句柄
        self.driver.switch_to.window(windows[1])

        # 进入订单列表
        WebDriverWait(self.driver, 10) \
            .until(lambda x: x.find_element_by_xpath('//*[@id="app"]/div/nav/ul/li[1]/div/a')).click()
        self.writeLog(self.workerNo, '已跳转至订单列表')
        # self.driver.get('https://guanjia.tujia.com/trademanagement/orderlist')

    # 检测方法最好可以覆盖doJob中所有页面中的元素标识
    def check(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 检测中....' % self.workerNo)
        # ======================起始页==========================
        self.driver.get(self.initUrl)
        time.sleep(3)
        # 用户名
        if not super().checkElement(By.Xpath,
                                    '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[1]/input'):
            return False

        # 密码
        if not super().checkElement(By.Xpath,
                                    '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[2]/input'):
            return False

        # 滚动条
        if not super().checkElement(By.Xpath, '//*[@id="nc_1_n1z"]'):
            return False

        # 提交按钮
        if not super().checkElement(By.Xpath, '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/button'):
            return False
        # ======================起始页==========================
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 检测完毕！' % self.workerNo)
        return True

    def close(self):
        if self.loginFlag:
            self.driver.get('https://passport.tujia.com/Landlord/Logout')
        super().close()