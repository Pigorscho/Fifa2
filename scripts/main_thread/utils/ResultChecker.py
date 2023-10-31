from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di
from scripts.utils.Colors import Colors

pics = di.get('pics')


class ResultChecker(FunctionNameDecorator):
    def __init__(self, mp, mpysin, panic):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin
        self.panic = panic

    @name
    def check_results(self):
        results = None

        no_results = self.mpysin.locate(**pics.no_results, find=False)
        if no_results:
            results = 'no_results'
        else:
            fourth_result = self.mpysin.locate(**pics.fourth_result, find=False)
            if fourth_result:
                results = 'too_many_results'
            else:
                if self.mpysin.locate(**pics.first_result):
                    results = 'good_results'
                else:
                    results = 'bad_results'
                    self.panic.increment()

        color = Colors.PURPLE
        if results == 'good_results':
            color = Colors.GREEN
        elif results == 'bad_results':
            color = Colors.RED
        self.mp.print(f'results: {results}', color=color)
        return results
