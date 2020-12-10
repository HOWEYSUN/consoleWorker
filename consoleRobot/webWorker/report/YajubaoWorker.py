import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from GlobalVar import cf, decrypt
from BasicWorker import ReportWorker


class YajubaoWorker(ReportWorker):
    """
        雅居宝渠道报备员，工号WF0104001，属于集团客服中心的第一个员工
        主要处理雅居宝wap端的报备工作
    """
    def __init__(self):
        self.loginFlag = False
        # 01集团
        # 04客服中心
        # 001自增编号
        super().__init__('WF01040001')

    def Validated(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker({}) report({})参数！'.format(self.workerNo, self.report))
            logging.debug('worker({}) customer({})参数！'.format(self.workerNo, self.report.customer))
            logging.debug('worker({}) project({})参数！'.format(self.workerNo, self.report.project))
        if self.report is None:
            return False

        if self.report.reportNo is None:
            return False

        if self.report.customer is None:
            return False

        if self.report.customer.tel is None:
            return False

        if self.report.project is None:
            return False

        if self.report.project.projectId is None:
            return False

        return True

    def close(self):
        # 若登录成功，则关闭时退出登录
        try:
            if self.loginFlag:
                self.driver.get('https://webapp.mypaas.com.cn/b2c/yk_qmyx/prod/user-setting?tenant_code=agile')
                WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector('.exit')).click()
            super().close()
        except Exception as e:
            self.logErrorMess(e, 'close function')
            return False

    def doLogin(self, waitElemet):
        try:
            waitElemet.send_keys(decrypt(cf.get('worker', 'yajubao.userName')))
            self.driver.find_element_by_xpath('//input[@type="password"]') \
                .send_keys(decrypt(cf.get('worker', 'yajubao.pwd')))
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/form/button').click()
            self.loginFlag = True
            # self.writeLog(self.report.reportNo, '登录成功')
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'doLogin function')
            return False
        except Exception as e:
            self.logErrorMess(e, 'doLogin function')
            return False

        return True

    def doSearch(self, element):
        try:
            element.click()
            self.driver.find_element_by_css_selector('.search-like').send_keys(self.report.project.name)
            self.driver.find_element_by_css_selector('.icon-search').click()
            # self.writeLog(self.report.reportNo, '搜索%s项目' % '金沙湾')
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'search page')
            return False
        except Exception as e:
            self.logErrorMess(e, 'search page')
            return False

    def setReportForm(self, element):
        try:
            customer = self.report.customer
            element.send_keys(customer.desc)
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[2]/div[1]/input')\
                .send_keys(customer.name)
            if int(customer.sex) == 0:
                self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[2]/div').click()
            else:
                self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[3]/div[2]/div[1]/div').click()

            self.driver.find_element_by_xpath('//input[@type="number"]').send_keys(customer.tel)
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'report submit page')
            return False
        except Exception as e:
            self.logErrorMess(e, 'report submit page')
            return False