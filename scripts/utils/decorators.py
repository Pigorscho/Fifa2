import inspect


def name(func):
    def wrapper(*args, **kwargs):
        # Get the names of the parameters for the function
        param_names = list(inspect.signature(func).parameters.keys())

        # Map them to their values; for args, skip the 'self' parameter
        params = list(zip(param_names[1:], args[1:])) + list(kwargs.items())

        # Convert all params to string, using __str__ for objects
        params_str = ", ".join(f"{name}={str(value)}" for name, value in params)

        line = inspect.currentframe().f_back.f_lineno

        frame = inspect.currentframe().f_back
        module = inspect.getmodule(frame)
        if module:
            module_name = module.__name__
        else:
            module_name = "unknown"

        print(f"{module_name} > l. {line}: {func.__name__}({params_str})")
        return func(*args, **kwargs)
    return wrapper


if __name__ == '__main__':
    from scripts.web import Players

    players = Players()

    class MyClass:

        @name
        def my_method(self, player):
            # print("Inside my_method")
            pass
        @name
        def another_method(self, param=42):
            # print(f"Inside another_method")
            pass
        @name
        def yet_another_method(self, obj):
            # print(f"Inside yet_another_method")
            pass

    class SomeObject:
        def __str__(self):
            return "SomeObject's string representation"

    # Example usage
    obj = MyClass()
    obj.my_method(players.get_player(0))
    obj.another_method(param=100)
    obj.yet_another_method(SomeObject())
