import logging


class BasicRobot:
    def __init__(self, worker):
        self.worker = worker

    def close(self):
        self.worker.close()

    def getWorkerNo(self):
        return self.worker.getWorkerNo()

    def doJob(self):
        self.worker.do()
