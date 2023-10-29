from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.DI.DI import di

pics = di.get('pics')


class ResultChecker(FunctionNameDecorator):
    def __init__(self, mp, mpysin):
        FunctionNameDecorator.__init__(self, mp.print)
        self.mp = mp
        self.mpysin = mpysin

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
                results = 'good_results'

        return results
