class BasicRobot:

    def __init__(self, worker):
        self.worker = worker

    def close(self):
        self.worker.close()

    def doJob(self):
        self.worker.do()
