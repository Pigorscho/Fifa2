
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

from scripts.game.Vendor2 import Vendor2

pics = di.get('pics')


class Vendor(FunctionNameDecorator):
    def __init__(self, mp, mpysin, slots, cremator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_vendor = Vendor2(mp, mpysin, cremator)
        self.mp = mp
        self.mpysin = mpysin
        self.slots = slots
        self.cremator = cremator

    @name
    def run(self, player, best_optimized_price):

        bought_counter = 0

        for trying_to_buy_player in range(50):

            if not self.slots.available:
                break  # inner loop

            if trying_to_buy_player != 0:
                self.refresh_results()  # plus minus kacka: die zweite
            if self.buy_player(player, best_optimized_price):
                self.sell_player()
                self.slots.available -= 1
                bought_counter += 1

        return bought_counter

    @name
    def refresh_results(self):
        """
        nach dem ersten mal spieler suchen: for i in range('Spielerkaufversuche'):
        click plus min_bid_price
        click plus min_buy_price
        search
        if no_results or player_purchase successfully:
            click minus min_bid_price
            click minus min_buy_price
            search

        :return:
        """
        pass

    @name
    def sell_player(self):
        """
        self.list_on_transfer_market()
        self.scroll_down_inside_selling_menu()
        self.enter_sell_price()
        self.send_to_auction()
        :return:
        """
        pass

    @name
    def buy_player(self, player, best_optimized_price):
        """
        self.click_player_result()
        self.click_buy_now()
        checked_purchase = self.approve_purchase()
        if checked_purchase:
            self.sell_player()
            self.back()
            rs.sleep(1)
            self.back()

        return checked_purchase

        :param player:
        :param best_optimized_price:
        :return:
        """
        pass
