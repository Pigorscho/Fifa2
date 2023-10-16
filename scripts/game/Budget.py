from scripts.main_thread.utils.decorators import FunctionNameDecorator, name

from scripts.DI.DI import di

pics = di.get('pics')
pil_regs = di.get('pil_regs')


class Budget(FunctionNameDecorator):
    def __init__(self, mpysin, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mpysin = mpysin
        self.mp = mp
        self.budget = 0
        self.budget_threshold = 420
        self.lower_budget_limit = 700

    @name
    def get_budget_limit(self):
        self.update_budget()
        return self.calculate_upper_limit()

    @name
    def do_budget_pause(self):
        return self.budget < self.budget_threshold

    @name
    def update_budget(self, new_budget):
        self.budget = self.mpysin.read_numbers(**pil_regs.budget)
        self.mp.print(f'updated budget to: {self.budget}')
        self.budget = new_budget



"""
price ranges :

500 - 1000         -  Risiko 1
1000 - 5000        -  Risiko 2
5000 - 10000       -  Risiko 3
10.000 - 25.000      -  Risiko 4   
25.000 - 50.000      -  Risiko 5
50.000 - 100.000     -  Risiko 6

link: https://www.futbin.com/players?page=1&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold



Rank:

Rank 1 - Budget:       0 -   100.000
Rank 2 - Budget: 100.000 -   200.000
Rank 3 - Budget: 200.000 -   350.000
Rank 4 - Budget: 350.000 -   500.000
Rank 5 - Budget: 500.000 - 1.000.000
... 
"""