
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

from scripts.game.Vendor2 import Vendor2

pics = di.get('pics')


class Vendor(FunctionNameDecorator):
    def __init__(self, mp, mpysin, slots, cremator, result_checker):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_vendor = Vendor2(mp, mpysin, cremator)
        self.mp = mp
        self.mpysin = mpysin
        self.slots = slots
        self.cremator = cremator
        self.result_checker = result_checker

        self.refresh_toggle = True  # plus/minus memory

    @name
    def run(self, player):

        bought_counter = 0

        for trying_to_buy_player in range(50):

            if not self.slots.available:
                break  # inner loop

            if trying_to_buy_player != 0:
                self.refresh_results()  # plus minus kacka: die zweite
            if self.buy_player(player):
                self.sell_player(player)
                self.slots.available -= 1
                bought_counter += 1
            self.sub_vendor.navigate_to_transfer_market_menu()

        return bought_counter

    @name
    def buy_player(self, player):
        bought = False

        results = self.result_checker.check_results()
        if results == 'good_results':
            arrows = self.sub_vendor.locate_arrows()
            chosen_result = self.sub_vendor.process_arrows(arrows)
            if chosen_result:
                self.mpysin.click(*chosen_result)
                self.sub_vendor.click_buy_now()
                bought = self.sub_vendor.approve_purchase(player)

        return bought


    @name
    def sell_player(self, player):
        self.sub_vendor.list_on_transfer_market()
        self.sub_vendor.scroll_down_inside_selling_menu()
        self.sub_vendor.enter_sell_price(player)
        self.sub_vendor.send_to_auction()

    @name
    def refresh_results(self):
        if self.refresh_toggle:
            self.refresh_toggle = False
            self.cremator.increment(pics.bid_price_increment_btn)
            self.cremator.increment(pics.sell_price_min_increment_btn)
        else:
            self.refresh_toggle = True
            self.cremator.decrement(pics.bid_price_decrement_btn)
            self.cremator.decrement(pics.sell_price_min_decrement_btn)
        search_btn = self.mpysin.locate(**pics.search_btn)
        if search_btn:
            self.mpysin.click(*search_btn)
