

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.game.CoinIndicator import CoinIndicator

pics = di.get('pics')
rs = di.get('rs')


class Vendor2(FunctionNameDecorator):
    def __init__(self, mp, mpysin, cremator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.coin_indicator = CoinIndicator(mp, mpysin)
        self.mp = mp
        self.mpysin = mpysin
        self.cremator = cremator

        self.coin_start_points_map = {
            0: (342, 640),
            1: (342, 1080),
            2: (342, 1515)
        }
        self.coin_approve_point = 365, 1245

    @name
    def increment_min_bid_price(self):
        self.cremator.increment(pics.bid_price_increment_btn)

    @name
    def decrement_min_bid_price(self):
        self.cremator.increment(pics.bid_price_decrement_btn)

    @name
    def increment_min_buy_price(self):
        self.cremator.increment(pics.sell_price_min_increment_btn)

    @name
    def decrement_min_buy_price(self):
        self.cremator.increment(pics.sell_price_min_decrement_btn)

    @name
    def navigate_to_transfer_market_menu(self):
        self.mpysin.back(dur=2)
        self.mpysin.back(dur=2)
        self.mpysin.check_point(**pics.transfers_menu_checkpoint)

    @name
    def locate_arrows(self):
        arrows = []
        self.mpysin.screen()
        pictures = [pics.first_result, pics.second_result, pics.third_result]
        for pic in pictures:
            arrow = self.mpysin.locate(**pic, screen=False)
            if arrow:
                arrows.append(arrow)

        return arrows

    @name
    def process_arrows(self, arrows):
        arrow = None

        numbers = []
        for i, arrow in enumerate(arrows):
            coin = self.mpysin.locate(**pics.__getattribute__(f'coin_result_{i}'), screen=False)
            start_point = self.coin_start_points_map[i]
            region = self.coin_indicator.calculate_region_by_coin(start_point, coin)
            number = self.mpysin.read_numbers(region, screen=False)
            numbers.append(number)
        if numbers:
            smallest_number = min(numbers)
            index = numbers.index(smallest_number)
            arrow = arrows[index]

        return arrow

    @name
    def click_buy_now(self):
        item_detail_checkpoint = self.mpysin.check_point(**pics.item_detail_checkpoint)
        if not item_detail_checkpoint:
            return
        buy_now_btn = self.mpysin.locate(**pics.buy_now_btn)
        self.mpysin.click(*buy_now_btn)
        confirm_buy_now_btn = self.mpysin.locate(**pics.confirm_buy_now_btn)
        self.mpysin.click(*confirm_buy_now_btn)

    @name
    def approve_purchase(self, player):
        approved = bool(self.mpysin.locate(**pics.purchase_approved))
        if approved:
            coin = self.mpysin.locate(**pics.approved_status_coin)
            region = self.coin_indicator.calculate_region_by_coin(self.coin_approve_point, coin)
            number = self.mpysin.read_numbers(region)
            player.bought_price = number
        return approved

    @name
    def list_on_transfer_market(self):
        list_on_transfer_market_btn = self.mpysin.locate(**pics.list_on_transfer_market_btn)
        self.mpysin.click(*list_on_transfer_market_btn, dur=1)

    @name
    def scroll_down_inside_selling_menu(self):
            self.mpysin.drag(535, 1452, 535, 145, 500) #ToDo check if this is correct
            rs.sleep(.5)

    @name
    def enter_sell_price(self, player):
        """
        click on input field 1 (700, 1075)
        enter sell price
        click on input field 2 (700, 1360)
        enter sell price
        :return:
        """
        self.mpysin.click(700, 1075)
        self.mpysin.typewrite(player.sell_price)
        self.mpysin.click(700, 1360)
        self.mpysin.typewrite(player.sell_price)

    @name
    def send_to_auction(self):
        list_for_transfer_btn = self.mpysin.locate(**pics.list_for_transfer_btn)
        if list_for_transfer_btn:
            self.mpysin.click(*list_for_transfer_btn, dur=1)

