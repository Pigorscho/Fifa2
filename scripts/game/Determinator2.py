import pyautogui
from time import sleep

from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.utils.PILRegs import reg_params

rs = di.get('rs')
pics = di.get('pics')
regs = di.get('pil_regs')


class Determinator2(FunctionNameDecorator):
    def __init__(self, mp, mpysin, emu, motivator):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin
        self.emu = emu
        self.motivator = motivator

    @name
    def reset_filters(self):
        reset_name_btn = self.mpysin.locate(**pics.reset_player_name_btn)
        if reset_name_btn:
            self.mpysin.click(*reset_name_btn)
        reset_filter_btn = self.mpysin.locate(**pics.reset_filter_btn)
        if reset_filter_btn:
            self.mpysin.click(*reset_filter_btn)
            # print(reset_filter_btn)
        self.scroll_down_inside_transfer_menu()
        expected_color = 252, 252, 247  # white
        reset_bid_price_pixel = 1288, 1538
        if self.mpysin.pixel_matches_color(reset_bid_price_pixel, expected_color, tolerance=25):
            self.mpysin.click(*reset_bid_price_pixel)
        reset_buy_price_pixel = 1287, 2144
        if self.mpysin.pixel_matches_color(reset_buy_price_pixel, expected_color, tolerance=25):
            self.mpysin.click(*reset_buy_price_pixel)
        self.scroll_up_inside_transfer_menu()

    @name
    def enter_name(self, player):
        type_player_name = self.mpysin.locate(**pics.type_player_name)
        if not type_player_name:
            raise Exception('type_player_name not found')
        x, y = type_player_name
        x += 500
        self.mpysin.click(x, y, dur=2)
        self.mpysin.typewrite(player.name, dur=2)
        self.mpysin.back()

    @name
    def select_searched_player(self, player):
        selected = False
        player_name_not_found = self.mpysin.locate(**pics.player_name_not_found, find=False)
        if player_name_not_found:
            self.motivator.punish_player(player)
            # ToDo nicetohave Blacklist Player
        else:
            sleep(.25)
            self.mp.print('looking for player results')
            self.mpysin.screen()
            self.mpysin.crop_img(
                regs.entered_player_name_reg['reg'], r'./pics/all_entered_player_name.png'
            )
            found_results = self.mpysin.wait_for(10, .1, **pics.player_name_search_results)
            if found_results:
                player_name_results = self.mpysin.locate_all(
                    **pics.all_entered_player_name, gray=True, center=False
                )
                for player_name_result in player_name_results:
                    x, y, xz, yz = player_name_result
                    # x += 670
                    a, b, az, bz = 940, y, 150, 100
                    # print(a, b, az, bz)
                    corresponding_rating = self.mpysin.read_numbers(reg_params((a, b, az, bz))['reg'])
                    self.mp.print(f'y: {y}, rating: {corresponding_rating}')
                    # print("1", bool('special' not in player.rating))
                    # print("2", bool(corresponding_rating == player.rating))
                    if 'special' not in player.quality and corresponding_rating == player.rating:
                        # print("clicking selected player")
                        self.mpysin.click(*pyautogui.center((a, b, az, bz)))
                        selected = True
            # print(f'generator_results: {selected}')
            return selected

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
        if self.mpysin.check_point(**pics.transfer_menu_scroll_to_price_checkpoint):
            self.max_buy_now_price = self.mpysin.locate(**pics.max_buy_price_btn)
            self.mpysin.click(*self.max_buy_now_price, 2)
            enter_price_checkpoint_2 = self.mpysin.check_point(**pics.enter_price_checkpoint)
            if enter_price_checkpoint_2:
                self.mpysin.typewrite(player.pc)
                self.mpysin.back()

    @name
    def search_player(self):
        search_btn = self.mpysin.wait_for(5, 1, **pics.search_btn)
        if search_btn:
            self.mpysin.click(*search_btn, 2)

    @name
    def get_price_from_input_field(self):
        if not self.mpysin.check_point(**pics.transfers_market_checkpoint):
            return
        self.mpysin.click(705, 2550)
        txt = self.emu.copy_text()
        if txt:
            txt = txt.replace(',', '').replace('.', '')
            txt = int(txt)
        return txt

    @name
    def get_best_optimized_price(self):
        return self.get_price_from_input_field()

    @name
    def get_determined_price(self):
        return self.get_price_from_input_field()

    @name
    def scroll_up_inside_transfer_menu(self):
        self.mpysin.drag(740, 770, 740, 2080, 500)
        rs.sleep(.5)
