from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.game.Budget import Budget

class RankSystem:
    def __init__(self, mpysin, mp, budget):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mpysin = mpysin
        self.mp = mp
        self.budget = ...

    @name
    def get_rank(self):
        if 0 <= self.budget <= 100000:
            return 1
        elif 100000 < self.budget <= 200000:
            return 2
        elif 200000 < self.budget <= 350000:
            return 3
        elif 350000 < self.budget <= 500000:
            return 4
        elif 500000 < self.budget <= 1000000:
            return 5
        else:
            return 0  # Invalid budget
    @name
    def can_use_rank(self, target_rank):
        current_rank = self.get_rank()
        return current_rank >= target_rank

    # Define the price ranges and convert them to strings
    price_ranges = {
        'Risiko 1': (500, 1000),
        'Risiko 2': (1000, 5000),
        'Risiko 3': (5000, 10000),
        'Risiko 4': (10000, 25000),
        'Risiko 5': (25000, 50000),
        'Risiko 6': (50000, 100000),
    }

    @name
    def generate_link(rank, price_ranges):
        # Function to generate the link based on price range
        if rank >= 1 and rank <= 5:
            lower_futbin_price, upper_futbin_price = price_ranges[f'Risiko {rank}']
            link = f"https://www.futbin.com/players?page=1&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold"
            return link
        else:
            return "Invalid Rank"

#
# if __name__ == '__main__':
#
# # Example usage:
#
# link = f"https://www.futbin.com/players?page=1&pc_price={lower_futbin_price}-{upper_futbin_price}&pos_type=all&sort=pc_price&order=asc&version=gold"
# budget = 150000  # You can change the initial budget value
# rank_system = RankSystem(budget)
# new_budget = 200000  # Set the new budget value
# rank_system.update_budget(new_budget)  # Update the budget
# current_rank = rank_system.get_rank()
# print(f"Updated Budget: {rank_system.budget}")
# print(f"Current Rank: {current_rank}")

