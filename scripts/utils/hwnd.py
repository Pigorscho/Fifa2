import win32gui


def get_hwnd_by_name(name):
    result = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)
    if result:
        return result[0]


def get_all_hwnds():
    result = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            result.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)
    if result:
        return result[0]
