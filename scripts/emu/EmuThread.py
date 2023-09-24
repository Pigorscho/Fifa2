from scripts.emu import emu_info
from scripts.android_automate.androidAutomate import Emulator



class EmuThread:
    def __init__(self, name=emu_info.os, port=5554):
        self.avd = Emulator(name, deviceId=f'emulator-{port}', verbose=False)
        self.avd.options = [
            "-no-boot-anim",
            "-noaudio",
            f"-port {port}"
        ]

    def run(self):
        self.avd.startEmulator()


if __name__ == '__main__':
    import sys

    emu = EmuThread(name=emu_info.os + sys.argv[1], port=int(sys.argv[2]))
    emu.run()

