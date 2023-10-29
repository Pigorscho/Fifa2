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
from scripts.game.Motivator import Motivator
from scripts.game.Players import Players
from scripts.main_thread.utils.Cremator import Cremator
from scripts.main_thread.utils.ResultChecker import ResultChecker
from scripts.game.Determinator import Determinator
from scripts.game.Vendor import Vendor

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
        self.motivator = Motivator(mp=self.mprint)
        self.players = Players(mp=self.mprint, motivator=self.motivator)
        self.cremator = Cremator(mp=self.mprint, mpysin=self.mpysin)
        self.result_checker = ResultChecker(mp=self.mprint, mpysin=self.mpysin)
        self.determinator = Determinator(
            mp=self.mprint, mpysin=self.mpysin, emu=self.emu,
            cremator=self.cremator, result_checker=self.result_checker, motivator=self.motivator
        )
        self.vendor = Vendor(
            mp=self.mprint, mpysin=self.mpysin, slots=self.slots,
            cremator=self.cremator, result_checker=self.result_checker
        )

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

                best_optimized_price = self.determinator.run(player)
                if not best_optimized_price:
                    self.motivator.punish_player(player)
                    break  # dont buy this player, go to next player

                bought_counter = self.vendor.run(player)
                if bought_counter > 2:
                    self.motivator.reward_player(player)  # aka player.performance++;
                elif not self.slots.available > 2:
                    self.motivator.punish_player(player)  # aka player.performance--;
            self.players.save_to_file()















