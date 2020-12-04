import logging
import time
import traceback

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import GlobalVar
from BasicWorker import BaobeiWorker


class YajubaoWorker(BaobeiWorker):
    """
        雅居宝渠道报备员，工号WF0104001，属于集团客服中心的第一个员工
        主要处理雅居宝wap端的报备工作
    """
    def __init__(self):
        loginUrl = 'https://webapp.mypaas.com.cn/b2c/yk_qmyx/prod/login?tenant_code=agile'
        logoutUrl = loginUrl
        self.loginFlag = False
        # 01集团
        # 04客服中心
        # 001自增编号
        super().__init__('WF01040001', loginUrl, logoutUrl)

    def logErrorMess(self, e, where):
        logging.error('worker({0}) work for report({1}) occur:{2} on ({3})！'.format(self.workerNo, self.report.reportNo, str(e), where))
        logging.error("error mess:%s" % traceback.format_exc())

    def do(self):
        customer = self.report.customer
        project = self.report.project

        if not self.report.project:
            logging.error('worker({}) 处理{}({})的报备信息缺少楼盘信息！'.format(self.workerNo, customer.name, customer.Id))
            return False

        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('进入初始页(%s)' % self.initUrl)
            logging.debug('开始对{}({})的报备信息进行处理！'.format(customer.name, customer.Id))
        if not self.doLogin():
            self.loginFlag = False
            return False
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector('.search-like')).click()
            self.driver.find_element_by_css_selector('.search-like').send_keys(project.name)
            self.driver.find_element_by_css_selector('.icon-search').click()
            if logging.root.isEnabledFor(logging.DEBUG):
                logging.debug('搜索%s项目' % project.name)
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_css_selector('.wxmessage-form-container__btn')) \
                .click()
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'search page')
            return False
        except Exception as e:
            self.logErrorMess(e, 'search page')
            return False

        # =====================填写报备信息 start================
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[6]/div/textarea')) \
                .send_keys(customer.desc)
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[2]/div[1]/input').send_keys(customer.name)
            if customer.sex == 0:
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
        # =====================填写报备信息 end================
        # 提交报备
        # self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[8]/form/button').click()

        self.driver.save_screenshot('%s.png' % self.report.reportNo)
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('进入报备页面并拍照成功！')

    # 检测方法最好可以覆盖doJob中所有页面中的元素标识
    def check(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 检测中....' % self.workerNo)
        # ======================登录页==========================
        if not self.doLogin():
            self.loginFlag = False
            return False
        # ======================登录页==========================

        # ======================搜索页==========================
        WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_css_selector('.search-like')).click()
        if not super().checkElement(By.CSS_SELECTOR, '.search-like'):
            return False

        if not super().checkElement(By.CSS_SELECTOR, '.icon-search'):
            return False

        self.driver.find_element_by_css_selector('.search-like').click()
        self.driver.find_element_by_css_selector('.search-like').send_keys('金沙湾')
        self.driver.find_element_by_css_selector('.icon-search').click()
        # ======================搜索页==========================

        # ======================报备提交页==========================
        time.sleep(2)
        self.driver.find_element_by_css_selector('.wxmessage-form-container__btn').click()
        # ======================报备提交页==========================
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug('worker(%s) 检测完毕！' % self.workerNo)
        return True

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

    def doLogin(self):
        try:
            super().doLogin()
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//input[@type="number"]')) \
                .send_keys(GlobalVar.decrypt(GlobalVar.cf.get('workShop', 'yajubao.userName')))
            self.driver.find_element_by_xpath('//input[@type="password"]') \
                .send_keys(GlobalVar.decrypt(GlobalVar.cf.get('workShop', 'yajubao.pwd')))
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/form/button').click()
            self.loginFlag = True
            if logging.root.isEnabledFor(logging.DEBUG):
                logging.debug('登录成功')
        except NoSuchElementException as ex:
            self.logErrorMess(ex, 'doLogin function')
            return False
        except Exception as e:
            self.logErrorMess(e, 'doLogin function')
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

