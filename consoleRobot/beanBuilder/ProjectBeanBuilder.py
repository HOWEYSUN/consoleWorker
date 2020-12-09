# utf-8
from beanBuilder.BasicBeanBuilder import BasicBeanBuilder
from beanBuilder.ProjectBean import Bean, Page, Location, Action


class ProjectBeanBuilder(BasicBeanBuilder):
    def __init__(self):
        super().__init__()
        self.beans = []

    def initBeans(self):
        for beanElement in self.getAllBean():
            self.beans.append(self.initBean(beanElement))

    def initBean(self, beanElement):
        bean = Bean(beanElement.get('workerNo'), beanElement.get('name'),
                    beanElement.get('moduleName'), beanElement.get('modulePackage'))
        if beanElement.get('callback'):
            bean.setCallback(beanElement.get('callback'))

        for page in self.getAllPages(beanElement):
            bean.addPage(self.initPage(page))
        return bean

    def initPage(self, pageElement):
        page = Page(pageElement.get('name'), pageElement.get('url'))
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


if __name__ == '__main__':
    builder = ProjectBeanBuilder()
    builder.initBeans()
    for bean in builder.beans:
        print(bean)
        for page in bean.pages:
            print(page)
            for location in page.locations:
                print(location)
                for action in location.actions:
                    print(action)
