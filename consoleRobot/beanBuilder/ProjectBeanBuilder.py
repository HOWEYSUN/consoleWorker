# utf-8
import importlib
import time

from selenium.webdriver.support.wait import WebDriverWait

from beanBuilder.BasicBeanBuilder import BasicBeanBuilder
from beanBuilder.ProjectBean import Bean, Page, Location, Action


class ProjectBeanBuilder(BasicBeanBuilder):
    def __init__(self):
        super().__init__()
        self._beans = dict()

    def getBeanByWorkerNo(self, workerNo):
        return self._beans.get(workerNo)

    def initBeans(self):
        for beanElement in self.getAllBean():
            projectBean = self.initBean(beanElement)
            self._beans[projectBean.workerNo] = projectBean

    def initBean(self, beanElement):
        bean = Bean(beanElement.get('workerNo'), beanElement.get('name'),
                    beanElement.get('moduleName'), beanElement.get('modulePackage'))
        if beanElement.get('callback'):
            bean.setCallback(beanElement.get('callback'))

        for page in self.getAllPages(beanElement):
            bean.addPage(self.initPage(page))
        return bean

    def initPage(self, pageElement):
        page = Page(pageElement.get('name'), pageElement.get('url'), pageElement.get('desc'))
        if pageElement.get('callback'):
            page.setCallback(pageElement.get('callback'))
        for location in self.getAllLocations(pageElement):
            page.addLocations(self.initLocation(location))
        return page

    def initLocation(self, locationElement):
        location = Location(locationElement.get('name'),
                            locationElement.get('by'),
                            locationElement.get('value'),
                            locationElement.get('waitUtil'),
                            locationElement.get('waitTime'))
        if locationElement.get('callback'):
            location.setCallback(locationElement.get('callback'))
        for actionElement in self.getAllActions(locationElement):
            action = Action(actionElement.get('by'),
                            actionElement.get('value'),
                            actionElement.get('timeSleep'))
            if actionElement.get('callback'):
                action.setCallback(actionElement.get('callback'))
            location.addActions(action)
        return location


#  单例模式
beanBuilder = ProjectBeanBuilder()
beanBuilder.initBeans()

if __name__ == '__main__':
    bean = beanBuilder.getBeanByWorkerNo('WF01140001')

    workerModuleObj = importlib.import_module('.' + bean.moduleName, bean.modulePackage)
    workerObj = getattr(workerModuleObj, bean.moduleName)
    worker = workerObj()

    for page in bean.pages:  # 遍历配置中的页面
        if page.url:
            worker.driver.get(page.url)  # 根据配置跳转至设置的URL

        if page.callback:  # 若存在回调函数则执行（注意：回调函数必须在当前类中存在！）
            worker.execCallbackFunc(worker, page.callback)

        for location in page.locations:  # 遍历页面中的定位
            if location.waitUtil:  # 支持显式等待
                element = WebDriverWait(worker.driver, int(location.waitTime)).until(
                    lambda x: x.find_element(location.by, location.value))
            else:
                element = worker.driver.find_element(location.by, location.value)

            if location.callback:  # 若存在回调函数则执行（注意：回调函数必须在当前类中存在！）
                worker.execCallbackFunc(worker, location.callback, element)

            for action in location.actions:  # 遍历每个定位中的操作
                if action.by is None:
                    continue

                worker.execCallbackFunc(element, action.by)
                if action.timeSleep:  # 支持强制等待
                    time.sleep(int(action.timeSleep))

                if action.callback:  # 若存在回调函数则执行（注意：回调函数必须在当前类中存在！）
                    worker.execCallbackFunc(worker, action.callback)