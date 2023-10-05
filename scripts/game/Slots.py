from scripts.DI.DI import di

pics = di.get('pics')
pil_regs = di.get('pil_regs')


class Slots():
    FAIL_COUNTER_THRESHOLD = 8

    def __init__(self, mpysin, mp):
        self.mpysin = mpysin
        self.mp = mp
        self.available = 1
        self.backup_available = self.available
        self.fail_clear_counter = 0

    def update_available_slots(self):
        self.backup_available = self.available
        current_items = self.mpysin.read_numbers(**pil_regs.current_items)
        current_selling = self.mpysin.read_numbers(**pil_regs.current_selling)
        current_sold = self.mpysin.read_numbers(**pil_regs.current_sold)
        self.available = 100 - current_items
        out = f'Free Transfer Slots: {self.available}, '
        out += f'Selling: {current_selling}, '
        out += f'Sold: {current_sold}'
        self.mp.print(out)

    def progress(self) -> bool:
        """
        checks if has more slots than before pause_controller
        function says no progress "anymore" if counter reaches self.FAIL_COUNTER_THRESHOLD
        """
        progressed = True

        if not self.available and not self.backup_available:
            self.fail_clear_counter += 1
            self.mp.print(f'incremented fail_clear_counter to {self.fail_clear_counter}')
        if self.fail_clear_counter >= self.FAIL_COUNTER_THRESHOLD:
            progressed = False

        return progressed
