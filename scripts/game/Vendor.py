
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.utils.Colors import Colors

from scripts.game.Vendor2 import Vendor2

pics = di.get('pics')


class Vendor(FunctionNameDecorator):
    VENDOR_THRESHOLD = 50

    def __init__(self, mp, mpysin, slots, cremator, result_checker, motivator, scrollator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_vendor = Vendor2(mp, mpysin, cremator, scrollator)
        self.mp = mp
        self.mpysin = mpysin
        self.slots = slots
        self.cremator = cremator
        self.result_checker = result_checker
        self.motivator = motivator
        self.scrollator = scrollator

        self.refresh_toggle = True  # plus/minus memory

    @name
    def run(self, player):

        bought_counter = 0

        for trying_to_buy_player in range(self.VENDOR_THRESHOLD):
            self.mp.print(
                f'trying_to_buy_player: {self.VENDOR_THRESHOLD - trying_to_buy_player} / {self.VENDOR_THRESHOLD}',
                color=Colors.YELLOW
            )

            if not self.slots.available:
                break  # inner loop

            if trying_to_buy_player != 0:
                self.refresh_results()  # plus minus kacka: die zweite
            if self.buy_player(player):
                self.sell_player(player)
                # self.sub_vendor.navigate_to_search_results()
                self.slots.available -= 1
                bought_counter += 1
            self.sub_vendor.navigate_to_transfer_market_menu()

        if bought_counter > 2:
            self.motivator.reward_player(player)  # aka player.performance++;
        elif self.slots.available > 2:
            self.motivator.punish_player(player)  # aka player.performance--;

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
        self.scrollator.scroll('sell_menu', 'down')
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
