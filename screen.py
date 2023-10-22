import os
import pyautogui
name = pyautogui.prompt('name')

path = rf'.\pics\{name}.png'
os.system(rf'adb -s emulator-5554 exec-out screencap -p > {path}')
if __name__ == '__main__':
    with open(r'.\scripts\utils\Pics.py', 'a') as f:
        f.write(f"    {name} = pic_params(r'{name}')\n")
    os.system(f'mspaint "{path}"')
