
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

from scripts.main_thread.utils.Cremator import Cremator
from scripts.game.Determinator2 import Determinator2

pics = di.get('pics')


class Determinator(FunctionNameDecorator):
    DETERMINATOR_THRESHOLD = 30

    def __init__(self, mp, mpysin, emu, cremator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_determinator = Determinator2(mp, mpysin, emu)
        self.mp = mp
        self.mpysin = mpysin
        self.emu = emu
        self.cremator = cremator

    def run(self, player):
        best_optimized_price = None

        determined_price = self.determine_best_price(player)  # plus minus kacka: die erste
        if determined_price:
            optimized_price = determined_price * .95  # transaction fee
            self.enter_optimized_price(optimized_price)
            for i in range(2):  # guarantee no loss
                self.decrement_search_price()  # click minus to decrement price
            best_optimized_price = self.sub_determinator.get_best_optimized_price()

        return best_optimized_price

    @name
    def determine_best_price(self, player):
        """

        :return: False if shall be punished and skipped onto next player
        """
        """
        # self.checkpoint transfer Market
        # enter player name
        # select due rating
        # select quality
        # select rarity
        # enter internet_buy price
        search_results
        if no results
            self.back() # -> entered search price criteria too low
            increment search price
        if too many results
            self.back() # -> entered search price criteria too high
            decrement search price
        if results good
            save price
            self.back()
        """
        determined_price = None

        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        self.sub_determinator.reset_filters()
        self.sub_determinator.enter_name(player)
        self.sub_determinator.select_searched_player(player)
        self.sub_determinator.select_quality(player)
        self.sub_determinator.select_rarity(player)
        self.sub_determinator.scroll_down_inside_transfer_menu()
        self.sub_determinator.enter_price(player)
        self.sub_determinator.search_player(player)

        for determining in range(self.DETERMINATOR_THRESHOLD):
            results = self.sub_determinator.check_for_results(player)
            if results == 'good_results':
                self.mpysin.back()
                determined_price = self.sub_determinator.get_determined_price(player)
                break

            elif results == 'no_results':
                self.mpysin.back()
                self.increment_search_price(player)
                self.search_player_again(player)
            elif results == 'too_many_results':
                self.mpysin.back()
                self.decrement_search_price(player)
                self.search_player_again(player)

        return determined_price

    @name
    def enter_optimized_price(self, optimized_price):
        """
        self.click max search price
        enter optimized price
        """
        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        self.sub_determinator.scroll_down_inside_transfer_menu()
        self.mpysin.click(705, 2550)
        self.mpysin.typewrite(optimized_price)

    @name
    def decrement_search_price(self):
        """
        self.click minus to decrement price
        """
        self.cremator.decrement(pics.sell_price_max_decrement_btn)

    @name
    def increment_search_price(self):
        """
        increment search price
        """
        self.cremator.increment(pics.sell_price_max_increment_btn)

    @name
    def search_player_again(self):
        """
        search player again
        """
        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        search_btn = self.mpysin.locate(**pics.search_btn)
        self.mpysin.click(*search_btn)

    # def refresh(self):
    #     pass
    #
    # def buy_player(self):
    #     pass
    #
    # def sell_player(self):
    #     pass
    #
    # def reward_player(self):
    #     pass
    #
    # def punish_player(self):
    #     pass
