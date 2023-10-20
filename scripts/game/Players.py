import json
from random import randint

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


class Players:
    def __init__(self):
        self.players = []

    def get_players(self, page, lower_futbin_price, upper_futbin_price):
        futbin = Futbin()
        player_info = []
        for name, rating, rarity, url in futbin.get_players(page, lower_futbin_price, upper_futbin_price):
            player_info.append((name, rating, rarity, url))

        # todo remember barometer + prio = 4 permutations
        player_info.sort()  # ToDo implement: match with current state of performance_barometer

        player_info = player_info[:randint(22, 30)]  # cut to random size

        for name, rating, rarity, url in player_info:
            futbin = Futbin()
            ps, pc = futbin.get_player(url)
            player = Player(name, rating, rarity, pc)
            self.players.append(player)
            yield player

    # def get_player(self, n):
    #     return self.players[n]

    def save_to_file(self):
        with open(r'.\vault\players.json', 'r', encoding='utf-8') as f:
            players_vault = json.load(f)
            for player in self.players:
                if not player.name in players_vault:
                    players_vault[player.name] = {player.quality: [player.to_dict()]}
                else:
                    if not player.quality in players_vault[player.name]:
                        players_vault[player.name][player.quality] = [player.to_dict()]
                    else:
                        players_vault[player.name][player.quality].append(player.to_dict())
        with open(r'.\vault\players.json', 'w', encoding='utf-8') as f:
            json.dump(players_vault, f, indent=4)
        self.players = []


if __name__ == '__main__':
    import os

    os.chdir('../..')

    players = Players()
    for player in players.get_players(1, 500, 1000):
        print(f'{player.name}: rating={player.rating}, rarity={player.rarity}, pc={player.pc}, url={player.url}')
    # players.save_to_file()
