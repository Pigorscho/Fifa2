from time import sleep
from threading import Thread

from scripts.main_thread.utils.ManuPysin import ManuPysin
from scripts.game.Preparations import Preparations
from scripts.utils.Secrets import Secrets
from scripts.game.Exceptions import ExceptionHandler

from scripts.game.Slots import Slots
from scripts.game.Budget import Budget
from scripts.game.Rank import Rank
from scripts.game.Pause import Pause
from scripts.game.ChronologyController import Chronology
from scripts.game.Futbin import Futbin
from scripts.game.Players import Players
# from scripts.game.Player import Player
# from scripts.game.Motivator import Motivator

from scripts.game.Exceptions import PanicException
from scripts.game.Exceptions import DuressException


class MainThread(Thread, ExceptionHandler):
    def __init__(self, info, account, settings):
        Thread.__init__(self)
        self.emu = info['emu']
        self.mprint = info['mprint']
        self.panic = info['panic']
        self.account_name = account
        self.color = settings['color']
        self.bg_color = settings['bg_color']
        self.port = settings['port']
        ExceptionHandler.__init__(self, mp=self.mprint)
        self.secrets = Secrets(name=self.account_name)
        self.mpysin = ManuPysin(emu=self.emu, mp=self.mprint, port=self.port, panic=self.panic)
        self.preparations = Preparations(secrets=self.secrets, mpysin=self.mpysin, mp=self.mprint)
        self.slots = Slots(mpysin=self.mpysin, mp=self.mprint)
        self.budget = Budget(mpysin=self.mpysin, mp=self.mprint)
        self.rank = Rank(mp=self.mprint, budget=self.budget)
        self.pause = Pause(mp=self.mprint, slots=self.slots, budget=self.budget)
        self.chronology = Chronology(mpysin=self.mpysin, mp=self.mprint, slots=self.slots)
        self.players = Players()
        # self.motivator = Motivator(self.mprint)

        self.threw_panic = False
        self.threw_duress = False

    def run(self):
        if not self.handle_exceptions(self.preparations.run):
            while True:
                if self.handle_exceptions(self.main):
                    return

    # def main_dev(self):
    #     self.panic.increment()
    #     sleep(.1)

    def main(self):
        self.chronology.clear_player_list()

        did_pause = self.pause.run()
        if did_pause:
            self.slots.update_available_slots()
            if not self.slots.progress():
                self.notify_human()

        self.rank.update_rank()
        budget_limit = self.budget.get_budget_limit(self.rank.rank)
        futbin = Futbin()
        pages = futbin.get_pages(*budget_limit)

        for page in range(1, pages + 1):
            for player in self.players.get_players(page, *budget_limit):

                if not self.slots.available:
                    return  # page/player loops

                bought_counter = 0
                best_price = self.determine_best_price(player)  # plus minus kacka: die erste
                if not best_price:
                    # player.punish()  # ToDo implement
                    break  # dont buy this player, go to next player
                optimized_price = best_price * .95  # transaction fee
                #ToDo Wo wird der Name und die Kaka eingegeben großes ToDo!!!
                # Determinator()
                self.enter_optimized_price(optimized_price)
                for i in range(2):  # guarantee no loss
                    self.lower_price()  # click minus to decrement price
                best_optimized_price = self.get_best_optimized_price()

                for trying_to_buy_player in range(50):

                    if not self.slots.available or bought_counter > 2:
                        break  # inner loop

                    if trying_to_buy_player != 0:
                        self.refresh()  # plus minus kacka: die zweite
                    if self.buy_player(best_optimized_price):
                        bought_counter += 1
                        self.slots.available -= 1
                        self.sell_player()

                if bought_counter > 2:
                    self.motivator.reward(player)  # aka player.performance++;
                elif not self.slots.available > 2:
                    self.motivator.punish(player)  # aka player.performance--;















