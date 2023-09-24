from scripts.utils.Print import Print as Print


class ManuPrint:
    def __init__(self, color, bg_color):
        self.color = color
        self.bg_color = bg_color
        self.p = Print()

    def print(self, to_print, color=None, bg_color=None, underline=False, bold=False, italic=False):
        if not color:
            color = self.color
        if not bg_color:
            bg_color = self.bg_color

        self.p.print(
            to_print=to_print,
            color=color, bg=bg_color,
            underline=underline, bold=bold, italic=italic
        )
