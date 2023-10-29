from scripts.DI.DI import di

pics = di.get('pics')


class Chronology:
    def __init__(self, mpysin, mp, slots):
        self.mp = mp
        self.mpysin = mpysin
        self.slots = slots

    def clear_player_list(self):
        if not self.navigate_to(pics.transfers_inactive_btn, pics.transfers_menu_checkpoint):
            return
        if not self.navigate_to(pics.transfers_list_btn, pics.transfers_list_checkpoint):
            return
        self.transfer_list_handle()
        if not self.navigate_to_simple(pics.transfers_menu_checkpoint):
            return
        self.slots.update_available_slots()
        if not self.navigate_to(pics.transfers_market_btn, pics.transfers_market_checkpoint):
            return

    def transfer_list_handle(self):
        for pic in [pics.clear_sold_players_btn, pics.re_list_players_btn]:
            location = self.mpysin.locate(**pic)
            if location:
                self.mpysin.click(*location)
                confirm = self.mpysin.wait_for(3, 1, **pics.confirm)
                if confirm:
                    self.mpysin.click(*confirm)

    def navigate_to(self, btn, check):
        button = self.mpysin.locate(**btn)
        if button:
            self.mpysin.click(*button)
            if self.mpysin.check_point(**check):
                return True

    def navigate_to_simple(self, check):
        self.mpysin.back()
        if self.mpysin.check_point(**check):
            return True


