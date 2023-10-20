import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scripts.web.Driver import Driver


class Browser:
    def __init__(self):
        try:
            self.start_browser()
        except Exception:
            self.apt_get_update()
            self.start_browser()

    def start_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")  # Set the window size
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Modify User-Agent to avoid detection
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        chrome_options.add_argument(f"user-agent={user_agent}")

        self.driver = webdriver.Chrome(executable_path=r'C:\Chromedriver\chromedriver', options=chrome_options)

    def close_browser(self):
        try:
            self.driver.close()
        except Exception:
            pass

    def apt_get_update(self):
        error = str(traceback.format_exc())
        if 'selenium.common.exceptions.SessionNotCreatedException' in error:
            print('mismatching chromedriver version detected')
            self.close_browser()
            version = None
            for line in error.splitlines():
                if line.startswith('Current browser version is '):
                    version = line.replace('Current browser version is ', '').replace(' with binary path', '')
                    version = ''.join(letter for letter in version if letter.isdigit())[:3]
                    break
            print(f'determined new chrome version: {version}')
            Driver(version).run()

    def find_element(self, by: 'str', val: 'str'):
        return self.driver.find_element(by, val)

    def find_elements(self, by: 'str', val: 'str', appearances): #ToDo check python version
        # appearances = [(contain, attribute), ...]
        check = lambda ele: all(ele and contains in ele.get_attribute(attr) for contains, attr in appearances)
        return [element for element in self.driver.find_elements(by, val) if check(element)]
