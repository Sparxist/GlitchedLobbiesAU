import pygetwindow as gw
import pyautogui
import time
from PIL import Image
import pytesseract
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pytesseract.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"

windows = [w for w in gw.getWindowsWithTitle("Among Us") if w.title == "Among Us"]
if not windows:
    raise RuntimeError("No window titled exactly 'Among Us' found.")
_win = windows[0]

def rel(x, y):
    """
    Convert normalized (0.0–1.0) coordinates within `window` to absolute screen coords.
    Clamps inputs to [0.0, 1.0].
    """
    left, top = _win.topleft
    width, height = _win.size

    x = min(max(x, 0.0), 1.0)
    y = min(max(y, 0.0), 1.0)

    screen_x = left + x * width
    screen_y = top  + y * height

    return int(screen_x//1), int(screen_y//1)


def click_lerp(x, y, do_click = True):
    screen_x, screen_y = rel(x, y)
    if do_click:
        pyautogui.click(screen_x, screen_y)

def wait_lerp(x, y, color, invert = False):
    ix, iy = rel(x, y)

    while True:
        matches = pyautogui.pixelMatchesColor(ix, iy, color)
        if (not invert and matches) or (invert and not matches):
            break
        time.sleep(0.03)

import pyautogui
import time

def capture_lerp(x1, y1, x2, y2):
    ix1, iy1 = rel(x1, y1)
    ix2, iy2 = rel(x2, y2)

    left = min(ix1, ix2)
    top = min(iy1, iy2)
    width = abs(ix2 - ix1)
    height = abs(iy2 - iy1)

    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    return screenshot

def macro_search(codes):
    _win.activate()
    time.sleep(0.5)
    while True:
        click_lerp(x=0.5,y=0.54)
        time.sleep(0.05)
        click_lerp(x=0.5,y=0.54)
        time.sleep(0.4)
        click_lerp(x=0.6,y=0.88)
        time.sleep(0.3)
        click_lerp(x=0.6,y=0.88)
        time.sleep(0.2)
        wait_lerp(x=0.79,y=0.215, color=(41,41,41))
        image = capture_lerp(x1=0.75,y1=0.2,x2=0.95,y2=0.35)
        bw = Image.new("RGB", image.size)
        pixels = image.load()
        out_pixels = bw.load()
        for i in range(image.width):
            for j in range(image.height):
                out_pixels[i, j] = (0, 0, 0) if pixels[i, j] == (0x2C, 0xEA, 0xC6) else (255, 255, 255)

        text = pytesseract.image_to_string(
            bw,
            config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ).strip()

        text = text.replace('Q', 'O')
        if text and text[-1] == 'O':
            text = text[:-1] + 'G'

        last4 = text[-4:]
        print(f"OCR result: {text}")

        # 8. Check halt condition

        codes = [i.replace("Q","O") for i in codes]

        if last4 in codes:
            print("Match!!")
            return
        
        print("Not Match")

        click_lerp(x=0.87,y=0.1)
        time.sleep(0.2)
        click_lerp(x=0.5,y=0.83)
        time.sleep(0.2)
        wait_lerp(x=0.79,y=0.215, color=(0,0,0), invert=True)
        time.sleep(0.7)