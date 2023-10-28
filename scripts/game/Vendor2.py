

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

pics = di.get('pics')


class Vendor2(FunctionNameDecorator):
    def __init__(self, mp, mpysin, cremator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin
        self.cremator = cremator

        self.refresh_toggle = False  # plus/minus memory

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
    def list_on_transfer_market(self):
        pass

    @name
    def scroll_down_inside_selling_menu(self):
        pass

    @name
    def enter_sell_price(self):
        pass

    @name
    def send_to_auction(self):
        pass

    @name
    def click_player_result(self):
        pass

    @name
    def click_buy_now(self):
        pass

    @name
    def approve_purchase(self):
        pass

    @name
    def sell_player(self):
        pass

