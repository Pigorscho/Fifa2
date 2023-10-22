from time import sleep

from scripts.game.Exceptions import DuressException
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name

from scripts.DI.DI import di

pics = di.get('pics')


class Playstore(FunctionNameDecorator):
    def __init__(self, mpysin, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mpysin = mpysin
        self.mp = mp

    def run(self):
        self.check_for_authentication_issue()
        if self.check_for_update():
            self.get_update()


    @name
    def check_for_authentication_issue(self):
        cannot_auth = self.mpysin.locate(**pics.cannot_authenticate)
        if cannot_auth:
            raise DuressException

    @name
    def check_for_update(self):
        return bool(self.mpysin.locate(**pics.software_update))

    @name
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