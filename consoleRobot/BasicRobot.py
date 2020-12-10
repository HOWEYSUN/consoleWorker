import logging


class BasicRobot:
    def __init__(self, worker):
        self.worker = worker

    def close(self):
        self.worker.close()

    def getWorkerNo(self):
        return self.worker.getWorkerNo()

    def doJob(self):
        if self.worker.Validated():
            self.worker.doBySop()
        else:
            logging.error('worker(%s)参数校验不通过！' % self.workerNo)
            pass
