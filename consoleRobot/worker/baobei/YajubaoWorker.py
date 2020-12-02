import time

from worker.basicWorker import BasicWorker


class YajubaoWorker(BasicWorker):
    def __init__(self):
        # 01集团
        # 04客服中心
        # 001自增编号
        super().__init__('WF0104001')

    def do(self):
        self.driver.find_element_by_xpath('//input[@type="number"]').send_keys('*****')
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys('*****')
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/form/button').click()

        time.sleep(2)
        self.driver.find_element_by_css_selector('.search-like').click()
        self.driver.find_element_by_css_selector('.search-like').send_keys('金沙湾')
        self.driver.find_element_by_css_selector('.icon-search').click()

        time.sleep(2)
        self.driver.find_element_by_css_selector('.wxmessage-form-container__btn').click()
