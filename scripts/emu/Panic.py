from scripts.game.Exceptions import PanicException
from scripts.game.Exceptions import DuressException


class Panic():
    PANIC_THRESHOLD = 20
    DURESS_THRESHOLD = 5

    def __init__(self, mp):
        self.mp = mp
        self.panic_counter = 0
        self.duress_counter = 0

    def increment(self):
        self.panic_counter += 1
        self.mp.print(
            f'incremented panic_counter to {self.panic_counter} | duress: {self.duress_counter}'
        )
        self.trigger_panic()
        self.trigger_duress()

    def trigger_panic(self):
        if self.duress_counter < self.DURESS_THRESHOLD:
            if self.panic_counter >= self.PANIC_THRESHOLD:
                self.panic_counter = 0
                self.duress_counter += 1
                self.mp.print('raising PanicException')
                raise PanicException

    def trigger_duress(self):
        if self.duress_counter >= self.DURESS_THRESHOLD:
            self.panic_counter = 0
            self.duress_counter = 0
            self.mp.print('raising DuressException')
            raise DuressException