import os

path = r'.\pics\screen-5554.png'
os.system(rf'adb -s emulator-5554 exec-out screencap -p > {path}')
if __name__ == '__main__':
    os.system(f'mspaint "{path}"')