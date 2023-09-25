

class Budget():
    def __init__(self, mp):
        self.mp = mp
        self.budget = 0
        self.budget_threshold = 420
        self.lower_budget_limit = 700

    def get_budget_limit(self):
        self.update_budget()
        return self.calculate_upper_limit()

    def do_budget_pause(self):
        return self.budget < self.budget_threshold

    def update_budget(self):
        pass  # ToDo
        # self.budget = ...
        self.mp.print(f'updated budget to: {self.budget}')

    def calculate_upper_limit(self):
        limit = None
        pass  # ToDo
        # self.budget ...
        self.mp.print(f'calculated limit: {limit}')
        return limit
