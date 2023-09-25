


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
        # Todo implement read numbers etc.
        # ...
        # self.available = some int  # is provided from read_numbers();
        # ...

    def progress(self) -> bool:
        """
        checks if has more slots than before pause
        function says no progress "anymore" if counter reaches self.FAIL_COUNTER_THRESHOLD
        """
        progressed = True

        if not self.available and not self.backup_available:
            self.fail_clear_counter += 1
            self.mp.print(f'incremented fail_clear_counter to {self.fail_clear_counter}')
        if self.fail_clear_counter >= self.FAIL_COUNTER_THRESHOLD:
            progressed = False

        return progressed

