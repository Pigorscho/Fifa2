import pyautogui
from time import sleep

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.utils.PILRegs import reg_params

rs = di.get('rs')
pics = di.get('pics')
regs = di.get('regs')



class Determinator2(FunctionNameDecorator):
    def __init__(self, mp, mpysin, emu):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin
        self.emu = emu

    @name
    def reset_filters(self):
        reset_name_btn = self.mpysin.locate(**pics.reset_player_name_btn)
        if reset_name_btn:
            self.mpysin.click(*reset_name_btn)
        reset_filter_btn = self.mpysin.locate(**pics.reset_filter_btn)
        if reset_filter_btn:
            self.mpysin.click(*reset_filter_btn)
            print(reset_filter_btn)
        self.scroll_down_inside_transfer_menu()
        reset_bid_price_btn = self.mpysin.wait_for(4, 1, **pics.reset_bid_price_btn)
        if reset_bid_price_btn:
            self.mpysin.click(*reset_bid_price_btn)
        reset_buy_price_btn = self.mpysin.wait_for(4, 1, **pics.reset_buy_price_btn)
        if reset_buy_price_btn:
            self.mpysin.click(*reset_buy_price_btn)
        self.scroll_up_inside_transfer_menu()

    @name
    def enter_name(self, player):
        type_player_name = self.mpysin.locate(**pics.type_player_name)
        if not type_player_name:
            raise Exception('type_player_name not found')
        self.mpysin.click(*type_player_name, dur=2)
        self.mpysin.typewrite(player.name, dur=2)
        self.mpysin.back()

    @name
    def select_searched_player(self, player):
        player_name_not_found = self.mpysin.locate(**pics.player_name_not_found, find=False)
        if player_name_not_found:
            # player.name # ToDo Blacklist Player
            pass
        else:
            sleep(.3)
            print('looking for player results')
            self.mpysin.screen()
            self.mpysin.crop_img(
                regs.entered_player_name_reg['reg'], r'./pics/all_entered_player_name.png'
            )
            found_results = self.mpysin.wait_for(10, 1, **pics.player_name_search_results)
            if found_results:
                player_name_results = self.mpysin.locate_all(
                    **pics.all_entered_player_name, gray=True, center=False
                )
                for player_name_result in player_name_results:
                    x, y, xz, yz = player_name_result
                    # x += 670
                    a, b, az, bz = 940, y, 100, 100
                    # print(a, b, az, bz)
                    corresponding_rating = self.mpysin.read_numbers(reg_params((a, b, az, bz))['reg'])
                    print(f'y: {y}, rating: {corresponding_rating}')
                    # print("1", bool('special' not in player.rating))
                    # print("2", bool(corresponding_rating == player.rating))
                    if 'special' not in player.quality and corresponding_rating == player.rating:
                        print("clicking selected player")
                        self.mpysin.click(*pyautogui.center((a, b, az, bz)))

    @name
    def select_quality(self, player):
        quality_menu_btn = self.mpysin.locate(**pics.quality_menu_btn)
        self.mpysin.click(*quality_menu_btn)
        searched_player_quality = self.mpysin.locate(**pics.player_quality_map[player.quality])
        if searched_player_quality:
            self.mpysin.click(*searched_player_quality, 2)

    @name
    def select_rarity(self, player):
        rarity_menu_btn = self.mpysin.locate(**pics.rarity_menu_btn)
        self.mpysin.click(*rarity_menu_btn)
        searched_player_rarity = self.mpysin.locate(**pics.player_rarity_map[player.rarity])
        if searched_player_rarity:
            self.mpysin.click(*searched_player_rarity, 2)

    def scroll_down_inside_transfer_menu(self):  # TODO Test
        self.mpysin.drag(535, 1452, 535, 145, 500)
        rs.sleep(.5)

    @name
    def enter_price(self, player):
        transfer_menu_scroll_to_price_checkpoint = self.mpysin.check_point(
            **pics.transfer_menu_scroll_to_price_checkpoint
        )
        if transfer_menu_scroll_to_price_checkpoint:
            # min_buy_price_btn = self.locate(**pics.min_buy_price_btn)
            # self.click(*min_buy_price_btn, 2)
            # enter_price_checkpoint = self.check_point(**pics.enter_price_checkpoint)
            # if enter_price_checkpoint:
            #     print(f'player price: {player.best_optimized_price}')
            #     self.typewrite(player.best_optimized_price, 1)
            #     self.back(1)
            self.max_buy_now_price = self.mpysin.locate(**pics.max_buy_price_btn)
            self.mpysin.click(*self.max_buy_now_price, 2)
            enter_price_checkpoint_2 = self.mpysin.check_point(**pics.enter_price_checkpoint)
            if enter_price_checkpoint_2:
                self.mpysin.typewrite(player.best_optimized_price)
                self.mpysin.back()

    @name
    def search_player(self):
        search_btn = self.mpysin.locate(**pics.search_btn)
        if search_btn:
            self.mpysin.click(*search_btn, 2)

    @name
    def check_for_results(self):
        no_results = self.mpysin.locate(**pics.no_results, find=False)
        if no_results:
            self.mpysin.back()
            result = 'no_results'
        else:
            results = self.mpysin.locate_all(**pics.result, find=False)
            if len(results) > 3:  # too_many_results
                self.mpysin.back()
                result = 'too_many_results'
            else:  # results_good
                result = 'good_results'

        return result

    @name
    def get_price_from_input_field(self):
        if not self.mpysin.checkpoint(**pics.transfers_market_checkpoint):
            return
        self.scroll_down_inside_transfer_menu()
        self.mpysin.click(705, 2550)
        self.emu.copy_text()

    @name
    def get_best_optimized_price(self):
        return self.get_price_from_input_field()

    @name
    def get_determined_price(self):
        return self.get_price_from_input_field()

    @name
    def scroll_up_inside_transfer_menu(self):
        self.mpysin.drag(535, 400, 535, 1490, 500)
        rs.sleep(.5)

