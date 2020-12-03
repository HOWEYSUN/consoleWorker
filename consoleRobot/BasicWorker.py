# 所有类型的工人的基类，每一个分类的工人都应继承此基类
import logging


class BasicWorker:
    # 初始化需要定义工人的工号
    # 编码规则为：WFXXYYZZZ
    # XX为集团编码01
    # YY为一级部门或子公司编码，具体对应编码参考部门编码
    # ZZZ为工人自增编号
    def __init__(self, workerNo):
        self.workerNo = workerNo
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'worker(%s) 初始化!' % workerNo)

    def close(self):
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.debug(f'worker(%s) 销毁!' % self.workerNo)
        pass

    def getWorkerNo(self):
        return self.workerNo

    # 自检
    # 需要爬取其他系统及网站的worker都应重写次方法，
    # 目的是给定时巡检程序判断该工人是否可用，若不可用应及时修正
    def check(self):
        return True

    # 参数检验
    def Validated(self):
        return True

    def doJob(self):
        pass
