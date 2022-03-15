import pyautogui
import keyboard
import re

FILENAME = 'prog.txt'
HOTKEY = 'shift+s'
ENTER_ADDRESS = 'f4'
WRITE = 'f5'


def hex_to_bin(a):
    return bin(int(a, 16))[2:].zfill(16)


program = []
startReg = hex_to_bin('0')
fileHash = ''


def pre_main():
    global startReg
    global program

    file = open(FILENAME)
    prog = file.read().split('\n')

    for item in prog:
        item = item.upper()
        parsed = re.findall("""^\\s*([0-9A-F]{3}):\\s*(\\+?)\\s*([0-9A-F]{4})\\s*$""", item)
        if len(parsed) != 1:
            continue
        reg, start, data = parsed[0]
        reg = '0' + reg
        if start == '+':
            startReg = reg
        program.append((reg, data))
        print(reg, data)


def main():
    for line in program:
        reg, data = line
        pyautogui.typewrite(reg)
        pyautogui.press(ENTER_ADDRESS)
        pyautogui.typewrite(data)
        pyautogui.press(WRITE)

    pyautogui.typewrite(startReg)
    pyautogui.press(ENTER_ADDRESS)
    pyautogui.alert('DONE!')


if __name__ == '__main__':
    pre_main()
    while True:
        keyboard.wait(HOTKEY)
        if 'БЭВМ' in pyautogui.getActiveWindowTitle():
            main()
