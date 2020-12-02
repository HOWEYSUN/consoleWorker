# app类型的工人, 基类需要初始化浏览器
from BasicWorker import BasicWorker


class BasicWebWorker(BasicWorker):
    def __init__(self, workerNo):
        super().__init__(workerNo)

    def close(self):
        super().close()

    def do(self):
        pass
