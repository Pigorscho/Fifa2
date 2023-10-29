from scripts.game.PauseController import PauseController


class Pause():
    def __init__(self, mp, slots, budget):
        self.pause_controller = PauseController(mp)
        self.mp = mp
        self.slots = slots
        self.budget = budget

    def run(self):
        did_pause = False

        if self.pause_controller.do_auto_pause():
            did_pause = True
            self.pause_controller.auto_pause()
        elif self.budget.do_budget_pause():
            did_pause = True
            self.pause_controller.auto_pause()

        elif not self.slots.available:
            did_pause = True
            self.pause_controller.forced_pause()

        return did_pause
