from webWorker.BasicWebWorker import BasicWebWorker


class BaobeiWorker(BasicWebWorker):
    def __init__(self, workerNo, loginUrl, logoutUrl):
        super().__init__(workerNo)
        self.initUrl = loginUrl
        self.endUrl = logoutUrl

    # 进入登录页
    def doLogin(self):
        self.driver.get(self.initUrl)

    def close(self):
        self.driver.get(self.endUrl)
        super().close()

    def setReport(self, report):
        self.report = report