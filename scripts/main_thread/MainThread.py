from time import sleep
from random import randint
from threading import Thread

from scripts.main_thread.utils.ManuPysin import ManuPysin
from scripts.game.Preparations import Preparations
from scripts.utils.Secrets import Secrets
# from scripts... import PauseController
# from scripts... import Slots
# from scripts... import Budget
# from scripts... import Futbin
# from scripts... import Players
# from scripts... import Player
# from scripts... import Motivator
#
from scripts.game.Exceptions import PanicException
from scripts.game.Exceptions import DuressException


class MainThread(Thread):
    def __init__(self, info, account, settings):
        Thread.__init__(self)
        self.emu = info['emu']
        self.mprint = info['mprint']
        self.panic = info['panic']
        self.account_name = account
        self.color = settings['color']
        self.bg_color = settings['bg_color']
        self.port = settings['port']
        self.secrets = Secrets(self.account_name)
        self.mpysin = ManuPysin(self.emu, self.mprint, self.port, self.panic)
        self.preparations = Preparations(self.secrets, self.mpysin, self.mprint)
        # self.pause = PauseController(self.mprint)
        # self.slots = Slots(self.mprint)
        # self.budget = Budget(self.mprint)
        # self.futbin = Futbin(self.mprint)
        # self.players = Players(self.mprint)
        # self.motivator = Motivator(self.mprint)

        self.threw_panic = False
        self.threw_duress = False

    def run(self):
        self.preparations.run() # ToDo
        while True:
            try:
                sleep(20)
                # self.budget.update_budget()
                # upper_budget_limit = self.budget.get_budget_limit()
                #
                # self.clear_playerlist()
                # self.slots.update_available_slots()
                #
                # did_pause = False
                # if self.pause.do_auto_pause() or self.budget.do_budget_pause():
                #     did_pause = True
                #     self.pause.auto_pause()
                #
                # elif not self.slots.available:
                #     did_pause = True
                #     self.pause.forced_pause()
                #
                # if did_pause:
                #     self.slots.update_available_slots()
                #     if not self.slots.progress():
                #         self.slots.notify_human()
                #
                # player_chunk = self.players.get_players(upper_budget_limit)  # Container: 30 players - information of one 'page'
                # player_chunk = self.players.sort_player_chunk(player_chunk)  # match with current state of performance_barometer
                # player_chunk = player_chunk[:randint(22, 30)]  # cut to random size
                #
                # for player_information in player_chunk:
                #
                #     if not self.slots.available:
                #         break  # player loop
                #
                #     player = Player(*player_information)
                #     bought_counter = 0
                #
                #     best_price = self.determine_best_price(player)  # plus minus kacka: die erste
                #     optimized_price = best_price * .95  # transaction fee
                #     self.enter_optimized_price(optimized_price)
                #     for i in range(2):  # guarantee no loss
                #         self.lower_price()  # click minus to decrement price
                #     best_optimized_price = self.get_best_optimized_price()
                #
                #     for trying_to_buy_player in range(50):
                #
                #         if not self.slots.available or bought_counter > 2:
                #             break  # inner loop
                #
                #         if trying_to_buy_player != 0:
                #             self.refresh()  # plus minus kacka: die zweite
                #         if self.buy_player(best_optimized_price):
                #             bought_counter += 1
                #             self.slots.available -= 1
                #             self.sell_player()
                #
                #     if bought_counter > 2:
                #         self.motivator.reward(player)  # aka player.performance++;
                #     elif not self.slots.available > 2:
                #         self.motivator.punish(player)  # aka player.performance--;
            except PanicException:
                self.threw_panic = True
                print('panic')
                break
            except DuressException:
                self.threw_duress = True
                print('duress')
                break















