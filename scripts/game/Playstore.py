from time import sleep

from scripts.game.Exceptions import DuressException

from scripts.DI.DI import di

pics = di.get('pics')


class Playstore:
    def __init__(self, mpysin, mp):
        self.mpysin = mpysin
        self.mp = mp

    def run(self):
        if self.check_for_update():
            self.get_update()

    def check_for_update(self):
        return bool(self.mpysin.locate(**pics.software_update))

    def get_update(self):
        ok = self.mpysin.locate(**pics.software_update_ok)
        if not ok:
            raise DuressException
        self.mpysin.click(*ok, dur=5)
        update = self.mpysin.locate(**pics.software_update_update)
        if not update:
            raise DuressException
        self.mpysin.click(*update)
        if not self.mpysin.wait_for(i=100, dur=2, **pics.software_update_cancel, reverse=True):
            raise DuressException
        confirm = self.mpysin.locate(**pics.software_update_confirm_btn)
        if not confirm:
            raise DuressException
        self.mpysin.click(*confirm, dur=5)