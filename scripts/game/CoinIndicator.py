from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

pics = di.get('pics')
regs = di.get('pil_regs')


class CoinIndicator(FunctionNameDecorator):
    def __init__(self, mp, mpysin):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin

    @name
    def calculate_region_by_coin(self, start_coords, coin):
        x, y, xz, yz = coin
        a, b = start_coords
        return  a, b, (x - a), yz

