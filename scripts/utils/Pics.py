def pic_params(pic, con=.9, reg=None):
    return {'pic': pic, 'con': con, 'reg': reg}


class Pics:
    quality_bronze = pic_params('quality_bronze')
    quality_silver = pic_params('quality_silver')
    quality_gold = pic_params('quality_gold')
    quality_special = pic_params('quality_special')
    rarity_menu_btn = pic_params('rarity_menu_btn')
    rarity_common = pic_params('rarity_common')
    rarity_rare = pic_params('rarity_rare')
    rarity_otw = pic_params('rarity_otw')
    rarity_totm = pic_params('rarity_totm')  # maybe more
    player_quality_map = {
        "Bronze": quality_bronze,
        "Silver": quality_silver,
        "Gold": quality_gold,
        "Special": quality_special
    }

    player_rarity_map = {
        "non-rare": rarity_common,
        "rare": rarity_rare,
        "Ones_to_watch": rarity_otw,
        "Team_of_the_week": rarity_totm
    }
    home_active_btn = pic_params('home_active_btn')
    home_inactive_btn = pic_params('home_inactive_btn')
    transfers_active_btn = pic_params('transfers_active_btn')
    transfers_inactive_btn = pic_params('transfers_inactive_btn')
    enter_pwd_field = pic_params('enter_pwd_field')
    homescreen = pic_params('homescreen')
    homescreen2 = pic_params('homescreen2')
    login_btn = pic_params('login_btn')
    sign_in_btn = pic_params('sign_in_btn')
    software_update = pic_params('software_update')
    software_update_ok = pic_params('software_update_ok')
    software_update_update = pic_params('software_update_update')
    software_update_cancel = pic_params('software_update_cancel')
    software_update_confirm_btn = pic_params('software_update_confirm_btn')
    home_menu_checkpoint = pic_params('home_menu_checkpoint')
    transfers_menu_checkpoint = pic_params('transfers_menu_checkpoint')
    transfers_list_checkpoint = pic_params('transfers_list_checkpoint')
    transfers_market_checkpoint = pic_params('transfers_market_checkpoint')
    transfers_list_btn = pic_params('transfers_list_btn')
    transfers_market_btn = pic_params('transfers_market_btn')

    clear_sold_players_btn = pic_params('clear_sold_players_btn')
    re_list_players_btn = pic_params('re_list_players_btn')

    confirm = pic_params('confirm')
    cannot_authenticate = pic_params('cannot_authenticate')

    bid_price_increment_btn = pic_params(r'increment_btn', reg=(3, 1622, 1427, 195))
    bid_price_decrement_btn = pic_params(r'decrement_btn', reg=(3, 1622, 1427, 195))

    sell_price_min_increment_btn = pic_params(r'increment_btn', reg=(3, 2240, 1427, 195))
    sell_price_min_decrement_btn = pic_params(r'decrement_btn', reg=(3, 2240, 1427, 195))

    sell_price_max_increment_btn = pic_params(r'increment_btn', reg=(3, 2456, 1427, 195))
    sell_price_max_decrement_btn = pic_params(r'decrement_btn', reg=(3, 2456, 1427, 195))

    search_btn = pic_params(r'search_btn', reg=(750, 1715, 640, 1160))
    reset_player_name_btn = pic_params(r'reset_player_name_btn')
    reset_filter_btn = pic_params(r'reset_filter_btn')
    reset_bid_price_btn = pic_params(r'reset_bid_price_btn', con=.99, reg=(1250, 1450, 186, 132))
    reset_buy_price_btn = pic_params(r'reset_buy_price_btn', con=.99, reg=(1250, 2080, 186, 132))
    type_player_name = pic_params(r'type_player_name')
    player_name_not_found = pic_params(r'player_name_not_found')
    quality_menu_btn = pic_params(r'quality_menu_btn')
    max_buy_price_btn = pic_params(r'max_buy_price_btn', reg=(200,2500, 200, 110))
    enter_price_checkpoint = pic_params(r'enter_price_checkpoint')
    no_results = pic_params(r'no_results')
    result = pic_params(r'result')
    player_name_search_results = pic_params(r'player_name_search_results')

    first_result = pic_params(r'result_arrow', reg=(1326, 478, 100, 150))
    second_result = pic_params(r'result_arrow', reg=(1326, 920, 100, 150))
    third_result = pic_params(r'result_arrow', reg=(1326, 1335, 100, 150))
    fourth_result = pic_params(r'result_arrow', reg=(1326, 1770, 100, 150))

    search_results_checkpoint = pic_params(r'search_results_checkpoint', reg=(405, 94, 653, 130))
    buy_now_btn = pic_params(r'buy_now_btn', reg=(360, 1870, 400, 133))
    confirm_buy_now = pic_params(r'confirm_buy_now', reg=(196, 1670, 133, 100))
    item_detail_checkpoint = pic_params(r'item_detail_checkpoint', reg=(452, 88, 556, 155))
    purchase_approved = pic_params(r'purchase_approved', reg=(326, 1162, 339, 100))

    list_on_transfer_market_btn = pic_params(r'list_on_transfer_market_btn')
    list_for_transfer_btn = pic_params(r'list_for_transfer_btn')
    approved_status_coin = pic_params(r'approved_status_coin')

    coin_buy_now = pic_params(r'approved_status_coin', reg=(580, 1230, 350, 120))
    coin_result_0 = pic_params(r'coin_result', reg=(440, 630, 350, 120))
    coin_result_1 = pic_params(r'coin_result', reg=(440, 1064, 350, 120))
    coin_result_2 = pic_params(r'coin_result', reg=(440, 1490, 350, 120))

    all_entered_player_name = pic_params(r'all_entered_player_name', con=.95, reg=(30, 800, 950, 700))
    transfer_menu_scroll_to_price_checkpoint = pic_params(r'transfer_menu_scroll_to_price_checkpoint')
