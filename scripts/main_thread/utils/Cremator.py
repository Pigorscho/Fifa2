

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

pics = di.get('pics')


class Cremator(FunctionNameDecorator):
    def __init__(self, mp, mpysin):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin

    @name
    def increment(self, btn):
        increment_btn = self.mpysin.locate(**btn)
        self.mpysin.click(*increment_btn)

    @name
    def decrement(self, btn):
        decrement_btn = self.mpysin.locate(**btn)
        self.mpysin.click(*decrement_btn)
