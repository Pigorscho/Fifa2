import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def get_players(self, page, lower_futbin_price, upper_futbin_price):  # ToDo hand budget instead of limits
        url = f"https://www.futbin.com/players?page={page}&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold"
        self.driver.get(url)
        cn = 'player_name_players_table'
        player_names = [name.text for name in self.driver.find_elements(By.CLASS_NAME, cn)]
        player_ratings = [rating.text for rating in self.driver.find_elements(By.CLASS_NAME, 'rating') if rating.text]
        player_urls = [url.get_attribute('href') for url in self.driver.find_elements(By.CLASS_NAME, cn)]
        self.close_browser()
        # for name, rating, url in zip(player_names, player_ratings, player_urls):
        #     print(f'{name}: rating={rating}, url={url}')
        return zip(player_names, player_ratings, player_urls)

    def get_player(self, url):
        self.driver.get(url)
        ps = self.driver.find_element(By.ID, 'ps-lowest-1').get_attribute('data-price')
        pc = self.driver.find_element(By.ID, 'pc-lowest-1').get_attribute('data-price')
        self.close_browser()
        # print(f'ps: {ps}, pc: {pc}')
        return ps, pc


if __name__ == '__main__':
    page = 1
    lower_futbin_price = 500
    upper_futbin_price = 1000
    browser = Browser()
    for i, (name, rating, url) in enumerate(browser.get_players(page, lower_futbin_price, upper_futbin_price)):
        browser = Browser()
        ps, pc = browser.get_player(url)
        print(f'{name}: rating={rating}, ps={ps}, pc={pc}, url={url}')
        if i > 0:
            break
    # url_to_scrape = "https://www.futbin.com/23/player/26261/karim-benzema"
    # url_to_scrape = "https://www.futbin.com/23/player/26261/Ramona-Bachmann"
    # print(browser.get_player(url_to_scrape))