# utf-8
import time

from BasicWorker import BasicWebWorker
from GlobalVar import cf, decrypt


class WfhtWorker(BasicWebWorker):
    """
    我房系统操作员，系技术中心的第一号员工
    主要操作我房后台的报备单获取等工作
    """
    def __init__(self):
        super().__init__('WF01030001')

    def doLogin(self, element):
        self.driver.find_element_by_id('account').send_keys(decrypt(cf.get('worker','wf.userName')))
        self.driver.find_element_by_id('password').send_keys(decrypt(cf.get('worker', 'wf.pwd')))
        element.click()
        time.sleep(2)
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass

    def switchIframe(self):
        time.sleep(1)
        iframe = self.driver.find_element_by_xpath('//*[@id="dinner-tab"]/div/div[2]/iframe')
        self.driver.switch_to.frame(iframe)

