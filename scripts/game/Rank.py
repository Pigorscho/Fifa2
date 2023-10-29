from scripts.main_thread.utils.decorators import FunctionNameDecorator, name


class Rank(FunctionNameDecorator):
    RANK_5 = 1000000
    RANK_4 = 500000
    RANK_3 = 350000
    RANK_2 = 200000
    RANK_1 = 100000

    def __init__(self, mp, budget):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.budget = budget
        self.rank = None

    @name
    def update_rank(self):
        """
        Determines the rank of an object based on its budget.

        The rank is determined by comparing the budget to predefined rank thresholds.
        The rank is represented as a tuple indicating the range of the budget.
        """
        if self.budget.budget > self.RANK_5:
            self.rank = 5
        elif self.budget.budget > self.RANK_4:
            self.rank = 4
        elif self.budget.budget > self.RANK_3:
            self.rank = 3
        elif self.budget.budget > self.RANK_2:
            self.rank = 2
        elif self.budget.budget > self.RANK_1:
            self.rank = 1
        else:
            self.rank = 0

    @name
    def test_get_url(self):
        """
        Function to generate the url based on price range
        :return:
        """
        if self.rank:
            lower_futbin_price, upper_futbin_price = self.rank
            url = f'https://www.futbin.com/players?page=1&pc_price={lower_futbin_price}-'
            url += f'{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold'
            return url
        else:
            raise Exception('Invalid Rank')


if __name__ == '__main__':
    class Budget:
        def __init__(self, budget):
            self.budget = budget

    class MP:
        def __init__(self):
            self.print = print

    mp = MP()
    budgets = [4200, 42000, 420000, 4200000, 42000000]

    for budget in budgets:
        b = Budget(budget)
        r = Rank(mp, b)
        # r.determine_rank()
        print(f'{budget}: {r.test_get_url()}')





























