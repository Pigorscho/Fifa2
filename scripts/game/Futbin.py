from selenium.webdriver.common.by import By

from scripts.web.Browser import Browser


class Futbin(Browser):
    def __init__(self):
        Browser.__init__(self)

    def get_pages(self, lower_futbin_price, upper_futbin_price):
        url = f"https://www.futbin.com/players?page=1&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold"
        self.driver.get(url)
        pages = int(self.driver.find_elements(By.CLASS_NAME, 'page-link')[-2].get_attribute('innerHTML'))
        self.close_browser()
        # print(f'pages: {pages}')
        return pages

    def get_players(self, page, lower_futbin_price, upper_futbin_price, quality='Gold'):  # ToDo hand budget instead of limits
        url = f"https://www.futbin.com/players?page={page}&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version={quality}"
        self.driver.get(url)
        cn = 'player_name_players_table'
        player_names = [name.text for name in self.driver.find_elements(By.CLASS_NAME, cn)]
        player_ratings = [rating.text for rating in self.driver.find_elements(By.CLASS_NAME, 'rating') if rating.text]
        player_urls = [url.get_attribute('href') for url in self.driver.find_elements(By.CLASS_NAME, cn)]
        player_rarities = [img.get_attribute('class').split(' ')[-1] for img in self.driver.find_elements(By.CLASS_NAME, 'player_img')]
        player_qualities = [quality for _ in range(len(player_names))]

        self.close_browser()
        # for name, rating, url in zip(player_names, player_ratings, player_urls, player_rarities):
        #     print(f'{name}: rating={rating}, url={url}, rarity={rarity}, quality={quality}')
        return zip(player_names, player_ratings, player_rarities, player_qualities, player_urls)

    def get_player(self, url):
        self.driver.get(url)
        ps = self.driver.find_element(By.ID, 'ps-lowest-1').get_attribute('data-price')
        pc = self.driver.find_element(By.ID, 'pc-lowest-1').get_attribute('data-price')
        # Find the parent element using CSS selector
        # rarity = ((self.driver.find_element(By.CSS_SELECTOR, '.breadcrumb-item.active')) ).get_attribute('innerHTML')#.find_element(By.TAG_NAME, 'span')).get_attribute('innerHTML').split('  ')[-1]
        #
        # # Find the sub-element (span in this case) within the parent element
        # span_element = parent_element.find_element(By.TAG_NAME, 'span')
        #
        # # Get the inner HTML or text from the span element
        # span_inner_html = span_element.get_attribute('innerHTML')
        #
        # rarity = self.driver.find_element(By.CLASS_NAME, 'breadcrumb-item.active').get_attribute('innerHTML').find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        self.close_browser()
        # print(f'ps: {ps}, pc: {pc}, rarity: {rarity}')
        return ps, pc


if __name__ == '__main__':
    lower_futbin_price = 500
    upper_futbin_price = 1000
    futbin = Futbin()
    pages = futbin.get_pages(lower_futbin_price, upper_futbin_price)
    print(f'pages: {pages}')

    for page in range(1, pages + 1):
        futbin = Futbin()
        for i, (name, rating, rarity, url) in enumerate(
                futbin.get_players(page, lower_futbin_price, upper_futbin_price)
        ):
            futbin = Futbin()
            ps, pc = futbin.get_player(url)
            print(f'{page} - {name}: rating={rating}, rarity={rarity}, ps={ps}, pc={pc}, url={url}')
            if i > 0:
                break
        if page > 1:
            break

    # url_to_scrape = "https://www.futbin.com/23/player/26261/karim-benzema"
    # url_to_scrape = "https://www.futbin.com/23/player/26261/Ramona-Bachmann"
    # print(browser.get_player(url_to_scrape))