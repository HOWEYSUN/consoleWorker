# utf-8
from PyInstaller.__main__ import run

if __name__ == '__main__':
    # 设置参数——携程数组，最后一个是入口文件，#'--hidden-import'就是隐式导入的包
    opts = ['-D',
            '--hidden-import', 'webWorker',
            '--clean',
            'testRobot.py']
    # 执行run函数
    run(opts)
