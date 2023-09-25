import inspect

from scripts.main_thread.utils.ManuPrint import ManuPrint

class NameDecorator(ManuPrint):
    def __init__(self, func):
        ManuPrint.__init__()
        self.func = func

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            param_names = list(inspect.signature(self.func).parameters.keys())
            params = list(zip(param_names, args)) + list(kwargs.items())
            params_str = ", ".join(f"{name}={str(value)}" for name, value in params)

            line = inspect.currentframe().f_back.f_lineno

            frame = inspect.currentframe().f_back
            module = inspect.getmodule(frame)
            if module:
                module_name = module.__name__
            else:
                module_name = "unknown"

            print(f"{module_name} > l. {line}: {self.func.__name__}({params_str})")
            return self.func(instance, *args, **kwargs)

        return wrapper

if __name__ == '__main__':
    class Players:
        def get_player(self, index):
            return f"Player-{index}"

    players = Players()

    class MyClass:
        @NameDecorator
        def my_method(self, player):
            pass

        @NameDecorator
        def another_method(self, param=42):
            pass

        @NameDecorator
        def yet_another_method(self, obj):
            pass

    class SomeObject:
        def __str__(self):
            return "SomeObject's string representation"

    obj = MyClass()
    obj.my_method(players.get_player(0))
    obj.another_method(param=100)
    obj.yet_another_method(SomeObject())
