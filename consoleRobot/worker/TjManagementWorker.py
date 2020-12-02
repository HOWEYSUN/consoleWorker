import time

from selenium.webdriver import ActionChains

from consoleRobot.worker.basicWorker import BasicWorker


class TjManagementWorker(BasicWorker):
    def __init__(self):
        # 01集团
        # 18住我房
        # 03自增编号
        super().__init__('WF0118001')

    def do(self):
        self.driver.get('https://passport.tujia.com/PortalSite/LoginPage/')

        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[1]/input').send_keys(
            '18898941303')
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/div[1]/div[2]/input').send_keys('wdjgy1688')
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

        self.driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[3]/section[1]/div[2]/button').click()
        time.sleep(3)
        self.driver.get('https://guanjia.tujia.com/trademanagement/orderlist')
