class PanicException(Exception):
    def __init__(self):
        Exception.__init__(self)


class DuressException(Exception):
    def __init__(self):
        Exception.__init__(self)


class ExceptionHandler:
    def __init__(self, mp):
        self.mp = mp
        self.threw_panic = False
        self.threw_duress = False

    def _handle_exceptions(self, exception):
        threw_exception = False

        if isinstance(exception, PanicException):
            self.mp.print('panic from within Thread')
            self.threw_panic = True
            threw_exception = True  # Signal to break the loop

        if isinstance(exception, DuressException):
            self.mp.print('duress from within Thread')
            self.threw_duress = True
            threw_exception = True  # Signal to break the loop

        return threw_exception  # Signal to continue the loop

    def handle_exceptions(self, func):
        try:
            func()
        except (PanicException, DuressException) as e:
            return self._handle_exceptions(e)