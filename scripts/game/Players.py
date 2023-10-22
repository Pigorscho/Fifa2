import json
from random import randint

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.game.Player import Player
from scripts.game.Futbin import Futbin


dummy_player_data = [
    {
        "name": "Djibril Sow",
        "rating": 80,
        "rarity": "Rare",
        "quality": "Gold",
        "min_buy_price": 1000,
        "eval_buy_price": 1100,
        "player_buy_price": 750,
        "sell_price": 1200
    },
    {
        "name": "Thorgan Hazard",
        "rating": 80,
        "rarity": "Rare",
        "quality": "Silver",
        "min_buy_price": 1000,
        "eval_buy_price": 1100,
        "player_buy_price": 1050,
        "sell_price": 1200
    },
    # ... Add more dummy data as required
]

# json_data = {
#     "player_name": {
#         "silver": [
#             {event1},
#             {event2}
#         ],
#         "gold": [
#             {event1...}
#         ],
#         "special-silver": [
#             ...
#         ],
#         "special-gold": [
#             ...
#         ]
#     },
#     ...
# }


class Players(FunctionNameDecorator):
    def __init__(self, mp, motivator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.motivator = motivator
        self.players = []

    @name
    def get_players(self, page, lower_futbin_price, upper_futbin_price):
        futbin = Futbin()
        player_chunk = []
        for name, rating, rarity, quality, url in futbin.get_players(page, lower_futbin_price, upper_futbin_price):
            player = Player(name, rating, rarity, quality, url)
            player_chunk.append(player)

        player_chunk = self.motivator.sort_player_chunk()

        player_chunk = player_chunk[:randint(20, 30)]  # cut to random size

        for player in player_chunk:
            futbin = Futbin()
            ps, pc = futbin.get_player(player.url)
            player.pc = pc
            self.players.append(player)
            yield player

    # def get_player(self, n):
    #     return self.players[n]

    @name
    def save_to_file(self):
        with open(r'.\vault\performance_list.json', 'r', encoding='utf-8') as f:
            players_vault = json.load(f)
        for player in self.players:
            if player.name not in players_vault:
                players_vault[player.name] = {player.quality: [player.to_dict()]}
            else:
                if player.quality not in players_vault[player.name]:
                    players_vault[player.name][player.quality] = [player.to_dict()]
                else:
                    players_vault[player.name][player.quality].append(player.to_dict())
        with open(r'.\vault\performance_list.json', 'w', encoding='utf-8') as f:
            json.dump(players_vault, f, indent=4)
        self.players = []


if __name__ == '__main__':
    import os

    os.chdir('../..')

    from scripts.game.Motivator import Motivator

    class MP:
        def __init__(self):
            self.print = print

    mp = MP()

    m = Motivator(mp)

    players = Players(mp, m)
    for player in players.get_players(1, 500, 1000):
        print(f'{player.name}: rating={player.rating}, rarity={player.rarity}, quality={player.quality}, pc={player.pc}')
    # players.save_to_file()
