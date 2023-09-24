from scripts.utils.Colors import Colors, _Colors


class Print:
    def print(self, to_print, color=None, underline=False, bold=False, italic=False, bg=None):
        if not color:
            color = Colors.CYAN
        out = f'{color}{to_print}{_Colors.END}'
        if underline:
            out = _Colors.UNDERLINE + out + _Colors.END
        if italic:
            out = _Colors.ITALIC + out + _Colors.END
        if bold:
            out = _Colors.BOLD + out + _Colors.END
        if bg:
            out = bg + out + _Colors.END
        print(out)


if __name__ == '__main__':
    p = Print()
    p.print('PINK', color=Colors.PINK)
    p.print('BLUE', color=Colors.BLUE)
    p.print('CYAN', color=Colors.CYAN)
    p.print('YELLOW', color=Colors.YELLOW)
    p.print('GREEN', color=Colors.GREEN)
    p.print('RED', color=Colors.RED)

    p.print('underlined PINK', color=Colors.PINK, underline=True)
    p.print('underlined BLUE', color=Colors.BLUE, underline=True)
    p.print('underlined CYAN', color=Colors.CYAN, underline=True)
    p.print('underlined YELLOW', color=Colors.YELLOW, underline=True)
    p.print('underlined GREEN', color=Colors.GREEN, underline=True)
    p.print('underlined RED', color=Colors.RED, underline=True)

    p.print('bold PINK', color=Colors.PINK, bold=True)
    p.print('bold BLUE', color=Colors.BLUE, bold=True)
    p.print('bold CYAN', color=Colors.CYAN, bold=True)
    p.print('bold YELLOW', color=Colors.YELLOW, bold=True)
    p.print('bold GREEN', color=Colors.GREEN, bold=True)
    p.print('bold RED', color=Colors.RED, bold=True)

    p.print('bold underlined PINK', color=Colors.PINK, underline=True, bold=True)
    p.print('bold underlined BLUE', color=Colors.BLUE, underline=True, bold=True)
    p.print('bold underlined CYAN', color=Colors.CYAN, underline=True, bold=True)
    p.print('bold underlined YELLOW', color=Colors.YELLOW, underline=True, bold=True)
    p.print('bold underlined GREEN', color=Colors.GREEN, underline=True, bold=True)
    p.print('bold underlined RED', color=Colors.RED, underline=True, bold=True)

    p.print('italic PINK', color=Colors.PINK, italic=True)
    p.print('italic BLUE', color=Colors.BLUE, italic=True)
    p.print('italic CYAN', color=Colors.CYAN, italic=True)
    p.print('italic YELLOW', color=Colors.YELLOW, italic=True)
    p.print('italic GREEN', color=Colors.GREEN, italic=True)
    p.print('italic RED', color=Colors.RED, italic=True)

    p.print('bg PINK', color=Colors.PINK, bg=Colors.BG_BLACK)
    p.print('bg BLUE', color=Colors.BLUE, bg=Colors.BG_RED)
    p.print('bg CYAN', color=Colors.CYAN, bg=Colors.BG_GREEN)
    p.print('bg YELLOW', color=Colors.YELLOW, bg=Colors.BG_ORANGE)
    p.print('bg GREEN', color=Colors.GREEN, bg=Colors.BG_BLUE)
    p.print('bg RED', color=Colors.RED, bg=Colors.BG_PURPLE)
