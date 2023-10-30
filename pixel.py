import os

from PIL import Image

path = rf'.\pics\pixel.png'
os.system(rf'adb -s emulator-5554 exec-out screencap -p > {path}')

pixel = 1288, 1538  # rgb: 101, 101, 99
# pixel = 1287, 2144  # rgb: 252, 252, 247


image = Image.open(path)
rgba = image.getpixel(pixel)
r, g, b, a = rgba
print(f'pixel{pixel}-rgb: {r}, {g}, {b}')