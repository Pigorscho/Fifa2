import os

path = r'.\pics\screen-5554.png'
os.system(rf'adb -s emulator-5554 exec-out screencap -p > {path}')
os.system(f'mspaint "{path}"')