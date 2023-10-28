import os
import string
import win32gui
import pyautogui
import clipboard
from time import sleep
from threading import Thread

from scripts.android_automate import androidAutomate
from scripts.utils.hwnd import get_hwnd_by_name


class Emu(Thread):
    def __init__(self, new, name, info):
        Thread.__init__(self)
        self.device = None
        self.new = new
        self.name = name
        self.coords = info['coords']
        self.port = info['port']
        self.window_name = info['emu_name']
        self.started = False

    def run(self):
        if self.new:
            command = rf'start python '
            command += r'.\scripts\emu\EmuThread.py '
            command += rf'{self.name} {self.port}'
            print(f"starting Emulator for '{self.name}' on port: {self.port}")
            os.system(command)
            for waiting in range(30):
                hwnd = get_hwnd_by_name(self.window_name)
                if hwnd:
                    break
                sleep(1)
        else:
            print(f"found Emulator for '{self.name}' on port: {self.port}")
        sleep(2)
        hwnd = get_hwnd_by_name(self.window_name)
        if not hwnd:
            raise Exception(f"could not find hwnd of newly started emulator '{self.window_name}'")
        self.started = True
        window = pyautogui.Window(hwnd)
        x, y, xz, yz = self.coords
        window.moveTo(x, y)
        window.resizeTo(xz, yz)
        win32gui.SetForegroundWindow(hwnd)
        self.device = androidAutomate.Device(f'emulator-{self.port}', verbose=False)
        self.device.clear_clipboard()

    def screen(self, image_path=None):
        # clean_single(self.port)
        if not image_path:
            image_path = f'screen-{self.port}.png'
        image_path = f'.\pics\\' + image_path
        os.system(
            rf'adb -s emulator-{self.port} exec-out screencap -p > {image_path}'
        )

    def launch(self, app):
        self.device.launchApp(app)
        sleep(2)

    def drag(self, *args, **kwargs):
        self.device.inputSwipe(*args, **kwargs)

    def tap(self, *args):
        self.device.inputTap(*args)

    @staticmethod
    def separate_string_updated(s):
        s = str(s)

        parts = []
        current_part = ""
        is_special = None

        for char in s:
            # Replace space with %s but still treat it as not special
            if char == ' ':
                char = '%s'

            # Check if the character is in ascii_letters or not
            char_is_special = char not in string.ascii_letters + string.digits and char != '%s'

            # If we're starting a new part or changing from letters to special characters or vice versa
            if is_special is None or is_special != char_is_special:
                if current_part:  # If there's any previous part, append it
                    parts.append({
                        'value': current_part,
                        'special': is_special
                    })
                current_part = char  # Start a new part
                is_special = char_is_special
            else:
                current_part += char  # Continue the current part

        # Append any leftover part
        if current_part:
            parts.append({
                'value': current_part,
                'special': is_special
            })

        return parts

    def input_text(self, text):
        self.device.inputText(text)

    def paste_text(self, text):
        if text == '.':
            self.device.keycodeEvent('56')
        elif text == '@':
            self.input_text('@')
        clipboard.copy(text)
        sleep(.1)
        self.device.keycodeEvent('279')  # KEYCODE_PASTE is 279

    def typewrite(self, to_type: str):
        parts = self.separate_string_updated(to_type)
        for part in parts:
            if part['special']:
                self.paste_text(part['value'])
                # print(f"pasted: {part['value']}")
            else:
                self.input_text(part['value'])
                # print(f"typed: {part['value']}")

    def copy_text(self):
        # todo nicetohave instead of one Windows-clipboard instead write to specific files
        os.system(f'adb -s emulator-{self.port} shell input keyevent 278')
        sleep(.06)
        return clipboard.paste()

    def enter(self):
        self.device.enter()

    def back(self):
        self.device.pressBack()

    def kill(self):
        os.system(f'adb -s emulator-{self.port} shell reboot -p')
        # os.system(f"adb -s emulator-{self.port} emu kill")

