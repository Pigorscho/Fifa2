"""



spieler in performance liste persistieren
spieler rewarden/punishen

playerchunk anhand der persistierten werte sortieren



"""
import json

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name


class Motivator(FunctionNameDecorator):
    # PROFITABILITY_THRESHOLD = 10
    PROFITABILITY_THRESHOLD = 1

    def __init__(self, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.path_to_motivation_list = r'.\vault\motivation_list.json'
        self.path_to_performance_list = r'.\vault\performance_list.json'
        self.motivation_list = {}
        self.performance_list = {}

    @name
    def load_motivation_list(self):
        with open(self.path_to_motivation_list, 'r', encoding='utf-8') as f:
            self.motivation_list = json.load(f)

    @name
    def load_performance_list(self):
        with open(self.path_to_performance_list, 'r', encoding='utf-8') as f:
            self.performance_list = json.load(f)

    @name
    def save_player_in_motivation_list(self, player):
        with open(self.path_to_motivation_list, 'r', encoding='utf-8') as f:
            motivation_list = json.load(f)
        motivation_list[player.name] = player.performance
        with open(self.path_to_motivation_list, 'w', encoding='utf-8') as f:
            json.dump(motivation_list, f, indent=4)
        self.load_motivation_list()

    def get_players_latest_performance(self, player):
        performance = 5
        if player.name in self.motivation_list:
            performance = self.motivation_list[player.name]
        return performance

    def get_players_profitability(self, player):
        """
        returns if is profitable in the long run range -2 to 2
        :return:
        """
        profitability = 0

        if player.name in self.performance_list and player.quality in self.performance_list[player.name]:
            entries = self.performance_list[player.name][player.quality]
            if len(entries) > self.PROFITABILITY_THRESHOLD:
                """
                # do math here
                durchschnitt(profits) * 3 / durchschnitt(bought_prices)
                """
                info = ((entry['profit'], entry['bought_price']) for entry in entries)
                profits, bought_prices = zip(*info)

                average_profit = sum(profits) / len(profits)
                average_bought_price = sum(bought_prices) / len(bought_prices)
                profitability = min(1, (average_profit * 3) / average_bought_price)
                new_min = -2
                new_max = 2
                profitability = (profitability * (new_max - new_min)) + new_min
                profitability = round(profitability)
                # todo del latestest entries until len(10)
        return profitability

    @name
    def reward_player(self, player):
        player.reward()
        self.save_player_in_motivation_list(player)

    @name
    def punish_player(self, player):
        player.punish()
        self.save_player_in_motivation_list(player)

    def sort_player_chunk(self, player_chunk):
        """
        should apply performance according to performance_list during sorting
        -> overwrites default performance if has performance persisted else default
        :return:
        """
        self.load_motivation_list()
        self.load_performance_list()

        for player in player_chunk:
            last_performance = self.get_players_latest_performance(player)
            profitability = self.get_players_profitability(player)
            player.performance = last_performance + profitability
        player_chunk.sort(key=lambda player: player.performance, reverse=True)

        return player_chunk


if __name__ == '__main__':
    import os
    os.chdir('../..')

    from scripts.game.Player import Player

    class MP:
        def __init__(self):
            self.print = print

    mp = MP()

    m = Motivator(mp)

    pl_c = [
        Player('Djibril Sow', 1, 'a', 'Gold', 'a'),
        Player('Thorgan Hazard', 1, 'a', 'Silver', 'a')
    ]
    pl_c = m.sort_player_chunk(pl_c)
    for player in pl_c:
        print(player.__dict__)
    # for player in pl_c:
    #     m.save_player_in_motivation_list(player)
