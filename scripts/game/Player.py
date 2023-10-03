
class Player:
    def __init__(
            self,
            name,
            rating, rarity, quality,
            min_buy_price, eval_buy_price,
            player_buy_price, sell_price,
            performance_barometer=5
    ):
        self.name = name
        self.rating = rating
        self.quality = quality
        self.rarity = rarity
        self.min_buy_price = min_buy_price
        self.eval_buy_price = eval_buy_price
        self.player_buy_price = player_buy_price
        self.sell_price = sell_price
        self.performance_barometer = performance_barometer
        self.bought_price = None

    def __str__(self):
        out = f'{self.name}, {self.quality}, {self.rarity}, '
        out += f'min: {self.min_buy_price}, eval: {self.eval_buy_price}, '
        out += f'buy: {self.player_buy_price}, sell: {self.sell_price}, '
        out += f'performance: {self.performance_barometer}'
        out += f', bought: {self.bought_price}'
        return out

    def punish(self):
        if self.performance_barometer > 0:
            self.performance_barometer -= 1

    def reward(self):
        if self.performance_barometer < 10:
            self.performance_barometer += 1

    def to_dict(self):
        return {
            'name': self.name,
            'quality': self.quality,
            'rarity': self.rarity,
            'min_buy_price': self.min_buy_price,
            'eval_buy_price': self.eval_buy_price,
            'player_buy_price': self.player_buy_price,
            'sell_price': self.sell_price,
            'performance_barometer': self.performance_barometer,
            'bought_price': self.bought_price,
        }

