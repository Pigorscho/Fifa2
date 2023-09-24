from time import sleep

from settings import settings
from scripts.emu import emu_info
from scripts.emu.Emu import Emu
from scripts.main_thread.MainThread import MainThread

from scripts.main_thread.utils.ManuPrint import ManuPrint
from scripts.emu.Panic import Panic

from scripts.utils.hwnd import get_hwnd_by_name


class EmuHandle:
    def __init__(self):
        self.emu_map = {}
        self.duressed = False

    def run(self):

        for account, info in settings.items():
            mprint = ManuPrint(info['color'], info['bg_color'])
            panic = Panic(mprint)
            self.emu_map[account] = {'panic': panic, 'mprint': mprint}

        self.start_emulators()

        while True:

            for account, info in self.emu_map.items():
                bot = info['bot']
                if bot.threw_panic:
                    print(f'@{account} found panic from outside thread')
                    bot.mpysin.close_app()
                    sleep(10)
                    bot = MainThread(info, account, settings[account])
                    info['bot'] = bot
                    bot.start()
                elif bot.threw_duress:
                    bot.mpysin.close_app()
                    sleep(10)
                    emu = self.emu_map[account]['emu']
                    emu.kill()
                    sleep(10)
                    self.duressed = True
                    self.start_emulators()
                    break

            sleep(5)

    def start_emulators(self):
        opened = False

        for account, info in settings.items():
            emu_thread_name = f"Android Emulator - {emu_info.os}{account}:{info['port']}"
            info['emu_name'] = emu_thread_name
            hwnd = get_hwnd_by_name(emu_thread_name)
            new = False if hwnd else True
            if new:
                opened = True

            self.emu_map[account]['emu'] = Emu(new=new, name=account, info=info)
            self.emu_map[account]['emu'].start()
            sleep(2)

        sleep(3)
        if opened:
            print('waiting for emu(s) to spawn')
            for account, info in self.emu_map.items():
                for waiting in range(30):
                    if info['emu'].started:
                        print(f"from outside: emulator for {account} started")
                        break
                    sleep(1)
        if self.duressed:
            sleep(30)
            self.duressed = False

        for account, info in settings.items():
            bot = MainThread(self.emu_map[account], account, info)
            self.emu_map[account]['bot'] = bot
            bot.start()

        return opened
