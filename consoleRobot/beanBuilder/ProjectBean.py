# utf-8


class Bean:
    def __init__(self, workerNo, name, moduleName, modulePackage):
        self.workerNo = workerNo
        self.name = name
        self.moduleName = moduleName
        self.modulePackage = modulePackage
        self.pages = []
        self.callback = None

    def __str__(self):
        return "workerNo:{}, name:{}, moduleName:{}, modulePackage:{}, callback:{}"\
            .format(self.workerNo, self.name, self.moduleName, self.modulePackage, self.callback)

    def __eq__(self, other) -> bool:
        return self.workerNo == other.workerNo

    def __hash__(self):
        return hash(self.workerNo)

    def addPage(self, page):
        self.pages.append(page)

    def setCallback(self, callback):
        self.callback = callback


class Page:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.callback = None
        self.locations = []

    def __str__(self):
        return "name:{}, url:{}, callback:{}".format(self.name, self.url, self.callback)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def addLocations(self, location):
        self.locations.append(location)

    def setCallback(self, callback):
        self.callback = callback


class Location:
    def __init__(self, name, by, value, waitUtil, waitTime):
        self.name = name
        self.by = by
        self.value = value
        self.waitUtil = waitUtil
        self.waitTime = waitTime
        self.callback = None
        self.actions = []

    def __str__(self):
        return "name:{}, by:{}, value:{}, waitUtil:{}, wailTime:{}, callback:{}"\
            .format(self.name, self.by, self.value, self.waitUtil, self.waitTime, self.callback)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def addActions(self, action):
        self.actions.append(action)

    def setCallback(self, callback):
        self.callback = callback


class Action:
    def __init__(self, by, value, timeSleep):
        self.by = by
        self.value = value
        self.timeSleep = timeSleep
        self.callback = None

    def __str__(self):
        return "by:{}, value:{}, timeSleep:{}, callback:{}"\
            .format(self.by, self.value, self.timeSleep, self.callback)

    def __hash__(self):
        return hash(self.name)

    def setCallback(self, callback):
        self.callback = callback