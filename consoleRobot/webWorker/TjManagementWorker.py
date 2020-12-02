import logging
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from consoleRobot.webWorker.BasicWebWorker import BasicWebWorker


class TjManagementWorker(BasicWebWorker):
    def __init__(self):
        # 01集团
        # 18住我房
        # 03自增编号
        super().__init__('WF0118001')
        self.initUrl = 'https://passport.tujia.com/PortalSite/LoginPage/'

    def do(self):
        self.driver.get(self.initUrl)

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[1]/input').send_keys(
            '*****')
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[2]/input').send_keys('*****')
        time.sleep(1)
        slideblock = self.driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        # 鼠标点击滑动块不松开
        ActionChains(self.driver).click_and_hold(slideblock).perform()
        # 将圆球滑至相对起点位置的 右边xx
        ActionChains(self.driver).move_by_offset(xoffset=50, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(self.driver).move_by_offset(xoffset=260, yoffset=0).perform()
        time.sleep(3)
        # 放开滑动块
        ActionChains(self.driver).release(slideblock).perform()
        time.sleep(3)

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/button').click()
        time.sleep(3)
        self.driver.get('https://guanjia.tujia.com/trademanagement/orderlist')

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
