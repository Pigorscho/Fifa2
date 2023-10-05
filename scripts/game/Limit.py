from scripts.main_thread.utils.decorators import FunctionNameDecorator, name


class CalcLimit(FunctionNameDecorator):
    # Mathematic sh** for the budget
    def __init__(self, mp):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp

    @name
    def run(self):
        pass