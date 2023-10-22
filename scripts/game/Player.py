
class Player:
    def __init__(
            self,
            name,
            rating,
            rarity,
            quality,
            url
    ):
        self.name = name
        self.rating = rating
        self.rarity = rarity
        self.quality = quality
        self.url = url
        self.pc = None
        self.min_buy_price = None
        self.eval_buy_price = None
        self.player_buy_price = None
        self.sell_price = None
        self.performance = None
        # self.last_performance = None
        # self.long_performance = None
        self.bought_price = None
        self.profit = None

    def __str__(self):
        out = f'{self.name}, {self.rating}, {self.pc}, {self.quality}, {self.rarity}, '
        out += f'min: {self.min_buy_price}, eval: {self.eval_buy_price}, '
        out += f'buy: {self.player_buy_price}, sell: {self.sell_price}, '
        out += f'performance: {self.performance}'
        # out += f', bought: {self.bought_price}'
        return out

    def punish(self):
        if self.performance > 0:
            self.performance -= 1

    def reward(self):
        if self.performance < 10:
            self.performance += 1

    def to_dict(self):
        return {
            'name': self.name,
            'rating': self.rating,
            'rarity': self.rarity,
            'quality': self.quality,
            'pc': self.pc,
            'min_buy_price': self.min_buy_price,
            'eval_buy_price': self.eval_buy_price,
            'player_buy_price': self.player_buy_price,
            'sell_price': self.sell_price,
            'performance': self.performance,
            'bought_price': self.bought_price,
            'profit': self.profit
        }


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