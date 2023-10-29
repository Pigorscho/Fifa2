from typing import List, Dict, Union, Tuple

import pyautogui
from PIL import Image
from time import sleep

from scripts.DI.DI import di
from scripts.utils.Colors import Colors
from scripts.main_thread.utils.decorators import FunctionNameDecorator, name
from scripts.utils.digits import recognize_digits

rs = di.get('rs')


class ManuPysin(FunctionNameDecorator):
    def __init__(self, emu, mp, port, panic):
        FunctionNameDecorator.__init__(self, mp.print)
        self.emu = emu
        self.mp = mp
        self.port = port
        self.panic = panic

    def screen(self, image_path=None):
        self.emu.screen(image_path)
        sleep(.01)

    def click(self, x, y, dur=1):
        self.emu.tap(x, y)
        rs.sleep(dur)

    def drag(self, *args, **kwargs):
        self.emu.drag(*args, **kwargs)
        dur = 1 if 'dur' not in args else args[args.index('dur')]
        rs.sleep(dur)

    def typewrite(self, to_type, dur=1):
        self.emu.typewrite(to_type)
        rs.sleep(dur)

    def enter(self, dur=1):
        self.emu.enter()
        rs.sleep(dur)

    def back(self, dur=1):
        self.emu.back()
        rs.sleep(dur)

    def pixel(self, x, y):
        self.screen()
        image = Image.open(rf'.\pics\screen-{self.port}.png')
        rgba = image.getpixel((x, y))
        r, g, b, a = rgba
        return r, g, b

    def pixel_matches_color(self, x, y, color, tolerance=0):
        current_rgb = self.pixel(x, y)
        current_r, current_g, current_b = current_rgb
        expected_r, expected_g, expected_b = color
        return (
                abs(current_r - expected_r) <= tolerance and
                abs(current_g - expected_g) <= tolerance and
                abs(current_b - expected_b) <= tolerance
        )

    def locate(self, pic, con=.9, reg=None, verbose=True, screen=True, find=True, center=True):
        if verbose:
            out = f"locating '{pic}'"
            if con >= .95:
                out += f" with high precision: '{con * 100}%'"
            self.mp.print(out)
        if '.png' not in pic:
            pic = pic + '.png'
        if screen:
            self.screen()
        try:
            location = pyautogui.locate(
                needleImage=rf'.\pics\{pic}', haystackImage=rf'.\pics\screen-{self.port}.png',
                confidence=con, region=reg
            )
        except Exception as e:
            self.mp.print(f"locate with pic: '{pic}' has encountered an error: {e}")
            location = None
        if location:
            if center:
                location = pyautogui.center(location)
            if verbose:
                color = Colors.GREEN if find else Colors.RED
                self.mp.print(f"found '{pic}' at {location}", color=color)
        else:
            if verbose:
                color = Colors.RED if find else Colors.GREEN
                self.mp.print(f"could not find '{pic}'", color=color)
        return location

    @name
    def locate_all(self, pic, con=.9, reg=None, center=True, gray=False):
        if '.png' not in pic:
            pic = pic + '.png'
        self.screen()
        try:
            locations = pyautogui.locateAll(
                needleImage=rf'.\pics\{pic}', haystackImage=rf'.\pics\screen-{self.port}.png',
                confidence=con, region=reg, grayscale=gray
            )
        except Exception as e:
            self.mp.print(f"locate_all with pic: '{pic}' has encountered an error: {e}")
            locations = []
        for location in locations:
            if center:
                location = pyautogui.center(location)
            yield location

    def wait_for(self, i, dur, pic, con=.9, reg=None, verbose=True, reverse=False):
        if verbose:
            out = f"waiting for '{pic}'"
            if reverse:
                out += ' in reverse mode'
            self.mp.print(out)
        location = None
        for _ in range(i):
            location = self.locate(pic=pic, con=con, reg=reg, verbose=False)
            if not reverse:
                if location:
                    color = Colors.RED if reverse else Colors.GREEN
                    self.mp.print(f"found '{pic}' at {location}", color=color)
                    break
            else:
                if not location:
                    color = Colors.GREEN if reverse else Colors.RED
                    self.mp.print(f"cannot find '{pic}' any longer", color=color)
                    break
            sleep(dur)
        if verbose:
            if not reverse and not location:
                self.mp.print(
                    f"could not find '{pic}' even though i expected to", color=Colors.RED
                )
            if reverse and location:
                self.mp.print(
                    f"can still find '{pic}' even though i expected not to", color=Colors.RED
                )
        return location

    def wait_for_multiple(
            self, i: int = 10, dur: Union[int, float] = 1,
            pics: List[
                Dict[str, Union[str, float, bool, None, Tuple[int, int, int, int]]]
            ] = None
    ) -> Union[None, bool, Tuple[int, int], Tuple[int, int, int, int]]:
        """
        call like so:

        result = self.wait_for_multiple(i=10, dur=1, [
            {**pics.my_picture1, 'find': False, 'center': False},
            {**pics.my_picture2, 'find': True, 'screen': False},
            **pics.my_picture3,
            ...
        ])
        if not result:
            raise Exception("couldn't match any given picture :/")
        elif result == True:  # 'elif result' is not specific enough
            # find = False picture has returned True
        else:
            self.click(*result)  # location returned


        :param i: similar to self.wait_for()
        :param dur: similar to self.wait_for()
        :param pics: all self.locate()-params possible
        :return: location || True on find=False  || False if nothing worked
        """
        out = False
        asserted = False

        for _ in range(i):
            for pic in pics:
                if 'find' in pic:
                    find = pic['find']
                else:
                    find = True
                location = self.locate(**pic)
                if (location and find) or (not location and not find):
                    out = location
                    asserted = True
                    self.mp.print(f"multi-check-pointed {pic['pic']}", color=Colors.GREEN)
                    break
                # elif not location and not find:
                #     out = True
                #     asserted = True
                #     self.mp.print(f"could not find {pic['pic']} any longer")
                #     break
            if asserted:
                break
            sleep(dur)

        return out

    def crop_img(self, reg, img_path):
        Image.open(rf'.\pics\screen-{self.port}.png').crop(reg).save(img_path)

    def read_numbers(self, reg, screen=True):
        if screen:
            self.screen()
        digit_path = f'.\pics\digits-{self.port}.png'
        self.crop_img(reg, digit_path)
        return recognize_digits(digit_path)

    @name
    def check_point(self, pic, con=.9, reg=None, reverse=False, i=5, dur=1):
        self.mp.print(f"checkpointing '{pic}'")
        location = self.wait_for(i, dur, pic, con, reg, reverse)
        checked = bool(location)
        # if (not reverse and not checked) or (reverse and checked):
        if not (reverse ^ checked):
            self.mp.print(f"could not assert '{pic}'", color=Colors.RED)
            self.panic.increment()
        else:
            self.mp.print(f"checkpoint '{pic}' reached successfully", color=Colors.GREEN)
        return checked

    @name
    def check_point_multiple(
        self, i: int = 10, dur: Union[int, float] = 1,
        pics: List[
            Dict[str, Union[str, float, bool, None, Tuple[int, int, int, int]]]
        ] = None
    ) -> bool:
        """
        call like so:

        if not self.check_point_multiple(i=10, dur=1, [
            {**pics.my_picture1, 'find': False, 'center': False},
            {**pics.my_picture2, 'find': True, 'screen': False},
            **pics.my_picture3,
            ...
        ]):
            # do sth to get to where u want because ure not there...

        :param i: similar to self.wait_for()
        :param dur: similar to self.wait_for()
        :param pics: all self.locate()-params possible
        :return: True if found any according to find
        """
        out = False

        result = self.wait_for_multiple(i=i, dur=dur, pics=pics)
        if not result:
            self.mp.print(f"could not assert any pic", color=Colors.RED)
            self.panic.increment()
        else:
            out = True

        return out



    @name
    def start_app(self):
        self.emu.device.launchApp('com.ea.gp.fifaultimate')
        sleep(5)

    @name
    def close_app(self):  # TODO implement
        self.emu.device.closeApp('com.ea.gp.fifaultimate')
        sleep(5)


