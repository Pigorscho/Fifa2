import os
import pyautogui


if __name__ == '__main__':
    name = pyautogui.prompt('name')
    path = rf'.\pics\{name}.png'
    if not name:
        print('aborted')
    else:
        os.system(rf'adb -s emulator-5554 exec-out screencap -p > {path}')
        with open(r'.\scripts\utils\Pics.py', 'a') as f:
            f.write(f"    {name} = pic_params(r'{name}')\n")
        os.system(f'mspaint "{path}"')
