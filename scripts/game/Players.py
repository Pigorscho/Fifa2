import json

from scripts.game.Player import Player
from scripts.web.Browser import Browser


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
        self.get_players()

    def get_players(self):
        for player_data in dummy_player_data:  # TODO add real data list here
            self.players.append(Player(
                player_data["name"],
                player_data["rating"],
                player_data["rarity"],
                player_data["quality"],
                player_data["min_buy_price"],
                player_data["eval_buy_price"],
                player_data["player_buy_price"],
                player_data["sell_price"]
            ))

    def get_player(self, n):
        return self.players[n]

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


if __name__ == '__main__':
    import os

    os.chdir('../..')

    players = Players()
    players.save_to_file()
