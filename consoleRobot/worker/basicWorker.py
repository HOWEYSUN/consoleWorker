from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BasicWorker:

    def __init__(self, workerNo):
        self.workerNo = workerNo
        print(f'basic worker init!')
        chrome_options = Options()
        chrome_options.add_argument('User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                                    'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"')
        chrome_options.add_argument('--start-maximized')  # 浏览器窗口最大化
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
        self.driver = webdriver.Chrome(options=chrome_options,
                                  executable_path='/Users/xudongchen/PycharmProjects/ExcelTool/python-test/chromedriver')
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

    def close(self):
        print(f'basic worker del!')
        self.driver.quit()

    def getDriver(self):
        return self.driver

    def do(self):
        pass
