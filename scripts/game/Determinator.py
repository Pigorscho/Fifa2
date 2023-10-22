from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

pics = di.get('pics')


class Determinator(FunctionNameDecorator):
    def __init__(self, mp, mpysin):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin

    @name
    def determine_best_price(self, player):
        """

        :return: False if shall be punished and skipped onto next player
        """
        """
        # self.checkpoint transfer Market
        # enter player name
        # select due rating
        # select quality
        # select rarity
        # enter internet_buy price
        search_results
        if no results
            self.back() # -> entered search price criteria too low
            increment search price
        if too many results
            self.back() # -> entered search price criteria too high
            decrement search price
        if results good
            save price
            self.back()
        """
        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        self.reset_filters()
        self.enter_name(player)
        self.select_searched_player(player)
        self.select_quality(player)
        self.select_rarity(player)
        self.scroll_down_inside_transfer_menu()
        self.enter_price(player)
        self.search_player(player)
        self.check_for_results(player)
        if results_good:
            self.save_price(player)
            self.back()
            self.lower_price()  # guarantee no loss
            optimized_price = self.save_new_determined_price(player)
            return optimized_price
        if no_results:
            self.back()
            self.increment_search_price(player)
            self.search_player_again(player)
        if too_many_results:
            self.back()
            self.decrement_search_price(player)
            self.search_player_again(player)


@name
def enter_optimized_price(self):
    """
    self.click max search price
    enter optimized price
    """
    pass


@name
def lower_price(self):
    """
    self.click minus to decrement price
    """
    pass


@name
def reset_filters(self):
    reset_name_btn = self.locate(**pics.reset_player_name)
    if reset_name_btn:
        self.click(*reset_name_btn)
    reset_filter_btn = self.locate(**pics.reset_filter_btn)
    if reset_filter_btn:
        self.click(*reset_filter_btn)
        print(reset_filter_btn)
    self.scroll_down_inside_transfer_menu()
    reset_bid_price_btn = self.wait_for(4, 1, **pics.reset_bid_price_btn)
    if reset_bid_price_btn:
        self.click(*reset_bid_price_btn)
    reset_buy_price_btn = self.wait_for(4, 1, **pics.reset_buy_price_btn)
    if reset_buy_price_btn:
        self.click(*reset_buy_price_btn)
    self.scroll_up_inside_transfer_menu()


def scroll_down_inside_transfer_menu(self):  # TODO Test
    self.drag(535, 1452, 535, 145, 500)
    rs.sleep(.5)


@name
def scroll_up_inside_transfer_menu(self):  # TODO Test
    self.drag(535, 400, 535, 1490, 500)
    rs.sleep(.5)


@name
def enter_name(self, player):
    type_player_name = self.mpysin.locate(**pics.type_player_name)
    if not type_player_name:
        raise Exception('type_player_name not found')
    self.mpysin.click(*type_player_name, dur=2)
    self.mpysin.typewrite(player.name, dur=2)
    self.back()


@name
def select_searched_player(self, player):
    player_name_not_found = self.locate(**pics.player_name_not_found, find=False)
    if player_name_not_found:
        # player.name # ToDo Blacklist Player
        pass
    else:
        sleep(.3)
        print('looking for player results')
        self.screen()
        self.crop_img(
            regs.entered_player_name_reg['reg'], r'./pics/all_entered_player_name.png'
        )
        found_results = self.wait_for(10, 1, **pics.player_name_search_results)
        if found_results:
            player_name_results = self.locate_all(
                **pics.all_entered_player_name, gray=True, center=False
            )
            for player_name_result in player_name_results:
                x, y, xz, yz = player_name_result
                x += 670
                a, b, az, bz = 700, y, 100, 100
                # print(a, b, az, bz)
                corresponding_rating = self.read_numbers(reg_params((a, b, az, bz))['reg'])
                print(f'y: {y}, rating: {corresponding_rating}')
                # print("1", bool('special' not in player.rating))
                # print("2", bool(corresponding_rating == player.rating))
                if 'special' not in player.quality and corresponding_rating == player.rating:
                    print("clicking selected player")
                    self.click(*pyautogui.center((a, b, az, bz)))


@name
def select_quality(self, player):
    quality_menu_btn = self.locate(**pics.quality_menu_btn)
    self.click(*quality_menu_btn)
    searched_player_quality = self.locate(**pics.player_quality_map[player.quality])
    if searched_player_quality:
        self.click(*searched_player_quality, 2)


@name
def select_rarity(self, player):
    rarity_menu_btn = self.locate(**pics.rarity_menu_btn)
    self.click(*rarity_menu_btn)
    searched_player_rarity = self.locate(**pics.player_rarity_map[player.rarity])
    if searched_player_rarity:
        self.click(*searched_player_rarity, 2)


@name
def enter_price(self, player):
    transfer_menu_scroll_to_price_checkpoint = self.check_point(
        **pics.transfer_menu_scroll_to_price_checkpoint
    )
    if transfer_menu_scroll_to_price_checkpoint:
        # min_buy_price_btn = self.locate(**pics.min_buy_price_btn)
        # self.click(*min_buy_price_btn, 2)
        # enter_price_checkpoint = self.check_point(**pics.enter_price_checkpoint)
        # if enter_price_checkpoint:
        #     print(f'player price: {player.player_buy_price}')
        #     self.typewrite(player.player_buy_price, 1)
        #     self.back(1)
        self.max_buy_now_price = self.locate(**pics.max_buy_price_btn)
        self.click(*self.max_buy_now_price, 2)
        enter_price_checkpoint_2 = self.check_point(**pics.enter_price_checkpoint)
        if enter_price_checkpoint_2:
            self.typewrite(player.player_buy_price)
            self.back()


@name
def search_player(self, player):
    search_btn = self.locate(**pics.search_btn)
    self.click(*search_btn, 2)


@name
def check_for_results(self, player):
    no_results = self.locate(**pics.no_results, find=False)
    if no_results:
        self.back()
        return False
    too_many_results = self.locate(**pics.too_many_results, find=False)
    if too_many_results:
        self.back()
        return False
    results_good = self.locate(**pics.results_good, find=False)
    if results_good:
        return True


@name
def save_price(self, player):
    """
    save price from input field
    :return:
    """
    pass


@name
def increment_search_price(self, player):
    """
    increment search price
    """
    pass


@name
def search_player_again(self, player):
    """
    search player again
    """
    pass


@name
def decrement_search_price(self, player):
    """
    decrement search price
    """
    pass


@name
def save_new_determined_price(self, player):
    """
    save new determined price
    """
    pass


@name
def back(self):
    """
    back
    """
    pass



# def refresh(self):
#     pass
#
# def buy_player(self):
#     pass
#
# def sell_player(self):
#     pass
#
# def reward_player(self):
#     pass
#
# def punish_player(self):
#     pass
