import inspect


def create_name_decorator(custom_print_func):
    class NameDecorator:
        def __init__(self, func):
            self.func = func

        def __get__(self, instance, owner):
            def wrapper(*args, **kwargs):
                param_names = list(inspect.signature(self.func).parameters.keys())
                params = list(zip(param_names, args)) + list(kwargs.items())
                params_str = ", ".join(f"{name}={str(value)}" for name, value in params)

                line = inspect.currentframe().f_back.f_lineno
                frame = inspect.currentframe().f_back
                module = inspect.getmodule(frame)
                module_name = module.__name__ if module else "unknown"

                custom_print_func(f"{module_name} > l. {line}: {self.func.__name__}({params_str})")
                return self.func(instance, *args, **kwargs)
            return wrapper
    return NameDecorator


def name(func):
    func._decorate = True
    return func


class FunctionNameDecorator:
    def __init__(self, custom_print):
        self.my_custom_print_func = custom_print
        NameDecorator = create_name_decorator(self.my_custom_print_func)

        for attr_name, attr_value in self.__class__.__dict__.items():
            if callable(attr_value) and getattr(attr_value, '_decorate', False):
                decorated_func = NameDecorator(attr_value)
                setattr(self, attr_name, decorated_func.__get__(self, self.__class__))


if __name__ == '__main__':
    class MyClass(FunctionNameDecorator):
        def __init__(self):
            FunctionNameDecorator.__init__(self, lambda text: print(f"Custom Print: {text}"))

        @name
        def my_method(self, player):
            pass

        @name
        def another_method(self, param=42):
            pass

        def yet_another_method(self, obj):
            pass

    class Players:
        def get_player(self, index):
            return f"Player-{index}"

    class SomeObject:
        def __str__(self):
            return "SomeObject's string representation"

    players = Players()
    obj = MyClass()
    obj.my_method(players.get_player(0))
    obj.another_method(param=100)
    obj.yet_another_method(SomeObject())
