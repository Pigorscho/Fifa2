# import pyautogui
#
# pyautogui.screenshot('screen.png')
# import os
# # os.system('adb shell input keyevent 56')
# os.system('adb shell input text "@"')


def f(x):
    return x ** x


def foo(x):
    return f(x)

def bar(x):
    return foo(x)

def foobar(x):
    return bar(x)

print(foobar(2))