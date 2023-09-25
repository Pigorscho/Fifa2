from time import sleep
from random import randint


class PauseController():
    MIN_ITERATIONS = 1
    MAX_ITERATIONS = 5
    AUTO_PAUSE_DUR = 30
    FORCE_PAUSE_DUR = 10

    def __init__(self, mp):
        self.mp = mp
        self.iterations = 0

    def auto_pause(self):
        self.iterations = 0
        for minutes in range(self.AUTO_PAUSE_DUR):
            self.mp.print(f'auto-pausing for another {self.AUTO_PAUSE_DUR - minutes} minute(s)')
            for seconds in range(60):
                sleep(1)

    def forced_pause(self):
        for minutes in range(self.FORCE_PAUSE_DUR):
            self.mp.print(f'force-pausing for another {self.FORCE_PAUSE_DUR - minutes} minute(s)')
            for seconds in range(60):
                sleep(1)

    def do_auto_pause(self):
        if self.iterations < self.MIN_ITERATIONS:
            do_pause = False
        elif self.iterations >= self.MAX_ITERATIONS:
            do_pause = True
        else:
            do_pause = randint(0, 1) == 0  # fifty fifty
            self.mp.print('magic 8 ball decided to take a nap')
        self.iterations += 1

        return do_pause
