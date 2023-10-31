from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

rs = di.get('rs')


class Scrollator(FunctionNameDecorator):
    def __init__(self, mp, mpysin):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin
        self.menu_scroll_coords_map = {
            'transfer_menu_down': (535, 1452, 535, 145, 100),
            'transfer_menu_up': (740, 770, 740, 2080, 100),
            'sell_menu_down': (535, 1452, 535, 145, 100)
        }

    @name
    def scroll(self, menu, direction, dur=.1):
        '''
        example call:
            scrollator = Scrollator()
            scrollator.scroll('transfer_menu', 'down')
        '''
        self.mpysin.drag(*self.menu_scroll_coords_map[menu + '_' + direction], dur=dur)
