
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

from scripts.main_thread.utils.Cremator import Cremator
from scripts.game.Determinator2 import Determinator2

pics = di.get('pics')


class Determinator(FunctionNameDecorator):
    DETERMINATOR_THRESHOLD = 15

    def __init__(self, mp, mpysin, emu, cremator, result_checker, motivator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_determinator = Determinator2(mp, mpysin, emu, motivator)
        self.mp = mp
        self.mpysin = mpysin
        self.emu = emu
        self.cremator = cremator
        self.result_checker = result_checker
        self.decrement_count = 0

    def run(self, player):
        best_optimized_price = None

        determined_price = self.determine_best_price(player)  # plus minus kacka: die erste
        player.determined_buy_price = determined_price
        if determined_price:
            optimized_price = determined_price * .95  # transaction fee
            self.enter_optimized_price(optimized_price)
            # for i in range(2):  # guarantee no loss
            self.decrement_search_price(i=2)  # click minus to decrement price
            best_optimized_price = self.sub_determinator.get_best_optimized_price()
        player.best_optimized_price = best_optimized_price
        sell_price = None
        if best_optimized_price:
            sell_price = best_optimized_price * 1.05
        else:
            self.mpysin.back()
        player.sell_price = sell_price

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

        if not self.mpysin.check_point(**pics.transfers_market_checkpoint):
            return
        self.sub_determinator.reset_filters()
        self.sub_determinator.enter_name(player)
        selected = self.sub_determinator.select_searched_player(player)
        if selected:
            self.sub_determinator.select_quality(player)
            self.sub_determinator.select_rarity(player)
            self.sub_determinator.scroll_down_inside_transfer_menu()
            self.sub_determinator.enter_price(player)
            self.sub_determinator.search_player()

            results = None
            for determining in range(self.DETERMINATOR_THRESHOLD):
                self.mp.print(f'determine_counter: {self.DETERMINATOR_THRESHOLD - determining}')
                results = self.result_checker.check_results()
                self.mp.print(f'results: {results}')
                self.mpysin.back()
                self.sub_determinator.scroll_down_inside_transfer_menu()
                if results == 'good_results':
                    determined_price = self.sub_determinator.get_determined_price()
                    break

                elif results == 'no_results':
                    self.decrement_count = 0
                    self.increment_search_price()
                elif results == 'too_many_results':
                    self.decrement_count *= 2
                    if self.decrement_count > 9:
                        self.decrement_count = 10
                    elif self.decrement_count == 0:
                        self.decrement_count = 1
                    self.decrement_search_price(i=self.decrement_count)

                self.search_player_again()
            if results == 'good_results':
                self.search_player_again()

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
    def decrement_search_price(self, i):
        """
        self.click minus to decrement price
        """
        self.cremator.decrement(pics.sell_price_max_decrement_btn, i)

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
        if not self.mpysin.check_point(**pics.transfers_market_checkpoint):
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
