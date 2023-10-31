
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.utils.Colors import Colors

from scripts.game.Determinator2 import Determinator2

pics = di.get('pics')


class Determinator(FunctionNameDecorator):
    DETERMINATOR_THRESHOLD = 15

    def __init__(self, mp, mpysin, emu, cremator, result_checker, motivator, scrollator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.sub_determinator = Determinator2(mp, mpysin, emu, motivator, scrollator)
        self.mp = mp
        self.mpysin = mpysin
        self.emu = emu
        self.cremator = cremator
        self.result_checker = result_checker
        self.decrement_count = 0
        self.motivator = motivator
        self.scrollator = scrollator

    @name
    def run(self, player):
        determined = False

        best_optimized_price = None
        determined_price = self.determine_best_price(player)  # plus minus kacka: die erste
        player.determined_buy_price = determined_price
        if determined_price:
            optimized_price = int(determined_price * .95)  # transaction fee
            self.enter_optimized_price(optimized_price)
            self.decrement_search_price(i=2)  # guarantee no loss
            best_optimized_price = self.sub_determinator.get_best_optimized_price()
            player.best_optimized_price = best_optimized_price
        sell_price = None
        if best_optimized_price:
            sell_price = int(determined_price * 1.05)
        player.sell_price = sell_price

        if not best_optimized_price:
            self.motivator.punish_player(player)
            if self.mpysin.locate(**pics.search_results_checkpoint):
                self.mpysin.back()
        else:
            self.search_player_again()
            determined = True

        return determined

    @name
    def determine_best_price(self, player):
        determined_price = None

        if not self.mpysin.check_point(**pics.transfers_market_checkpoint):
            return
        self.sub_determinator.reset_filters()
        self.sub_determinator.enter_name(player)
        selected = self.sub_determinator.select_searched_player(player)
        if selected:
            self.sub_determinator.select_quality(player)
            self.sub_determinator.select_rarity(player)
            self.scrollator.scroll('transfer_menu', 'down')
            self.sub_determinator.enter_price(player)
            self.sub_determinator.search_player()

            results = None
            for determining in range(self.DETERMINATOR_THRESHOLD):
                self.mp.print(
                    f'determine_counter: {self.DETERMINATOR_THRESHOLD - determining} / {self.DETERMINATOR_THRESHOLD}',
                    color=Colors.YELLOW
                )
                results = self.result_checker.check_results()
                self.mpysin.back()
                self.scrollator.scroll('transfer_menu', 'down')
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
            # if results == 'good_results':
            #     self.search_player_again()

        return determined_price

    @name
    def enter_optimized_price(self, optimized_price):
        """
        self.click max search price
        enter optimized price
        """
        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        self.mpysin.click(705, 2550)
        self.mpysin.typewrite(optimized_price)
        self.mpysin.back()

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
