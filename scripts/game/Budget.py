from scripts.main_thread.utils.decorators import FunctionNameDecorator, name

from scripts.DI.DI import di

pics = di.get('pics')
pil_regs = di.get('pil_regs')


class Budget(FunctionNameDecorator):
    BUDGET_LIMIT_5 = (50000, 100000)
    BUDGET_LIMIT_4 = (25000, 50000)
    BUDGET_LIMIT_3 = (10000, 25000)
    BUDGET_LIMIT_2 = (5000, 10000)
    BUDGET_LIMIT_1 = (1000, 5000)
    BUDGET_LIMIT_0 = (500, 1000)

    def __init__(self, mpysin, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mpysin = mpysin
        self.mp = mp
        self.budget = 0
        self.budget_threshold = 420
        self.lower_budget_limit = 700

    @name
    def do_budget_pause(self):
        return self.budget < self.budget_threshold

    @name
    def update_budget(self):
        self.budget = self.mpysin.read_numbers(**pil_regs.budget)
        self.mp.print(f'updated budget to: {self.budget}')

    def get_budget_limit(self, rank):
        if rank == 5:
            budget_limit =  self.BUDGET_LIMIT_5
        elif rank == 4:
            budget_limit =  self.BUDGET_LIMIT_4
        elif rank == 3:
            budget_limit =  self.BUDGET_LIMIT_3
        elif rank == 2:
            budget_limit =  self.BUDGET_LIMIT_2
        elif rank == 1:
            budget_limit =  self.BUDGET_LIMIT_1
        else:
            budget_limit =  self.BUDGET_LIMIT_0

        return budget_limit
