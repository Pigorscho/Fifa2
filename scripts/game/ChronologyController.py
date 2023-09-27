
"""
 self.arrived_in_menu(menu_btn,transfer_menu_checkpoint)
        read_numbers()
        self.arrived_in_menu(transfer_list_btn, transfer_list_checkpoint)
            self.clear_transfer_list
            self.relist_players
        self.back
        self.arrived_in_menu(transfer_market_btn, transfer_market_checkpoint)

        self.enter_player_data()
            self.reset_filters()
            self.enter_name(player)
            self.select_searched_player(player)
            self.select_quality(player)
            self.select_rarity(player)
            self.scroll_down_inside_transfer_menu()
            self.enter_price(player)

        self.search_filtered_player()
            self.unhappy_results()
            self.too_few_results()
            self.too_many_results()
            self.buy_player()

        self.buy_player()
            self.click_player_result()
            self.click_buy_now_btn()
            self.approved_purchase()

        self.list_player_on_transfermarket()
            self.list_on_transfer_market()
            self.scroll_down_inside_selling_menu()
            self.enter_sell_price_in_sell_menu()
            self.send_to_auction_house()

"""

class Chronology:
    def __init__(self, mp, mpysin):
        self.mp = mp
        self.mpysin = mpysin

    def run(self):
        if not self.move_to_transfer_menu():
            return
        self.read_numbers()
        # an der stelle schon in TransferList
        self.clear_player_list()
        self.checkpoint(*pics.transfer_menu_checkpoint)
        if not self.move_to_transfer_market():
            return
        # an der Stelle schon in TransferMarket
        self.enter_player_data()







    def clear_player_list(self):
        clear_sold_players_btn = self.locate(**pics.clear_sold_players_btn)
        if clear_sold_players_btn:
            self.click(*pics.clear_sold_players_btn)
        relist_players_btn = self.locate(**pics.relist_players_btn)
        if relist_players_btn:
            self.click(*pics.relist_players_btn)
        self.back()

    def self.enter_player_data(self)
        self.reset_filters()
        self.enter_name(player)
        self.select_searched_player(player)
        self.select_quality(player)
        self.select_rarity(player)
        self.scroll_down_inside_transfer_menu()
        self.enter_price(player)

