import pyautogui
import keyboard
import re

FILENAME = 'prog.txt'
HOTKEY = 'shift+s'
ENTER_ADDRESS = 'f4'
WRITE = 'f5'


def hex_to_bin(a):
    return bin(int(a, 16))[2:].zfill(16)


def bin_to_hex(a):
    return hex(int(a, 2))[2:].zfill(3).upper()


program = []
startReg = hex_to_bin('0')
fileHash = ''


def sum_hex(a, b):
    return hex((int(a, 16) + int(b, 16)) + 1)[2:]


def data_type(comm, data):
    tmp = hex_to_bin(data)[::-1]
    # return tmp
    if tmp[11] == '0':
        return f'${bin_to_hex(tmp[10::-1])}'
    if tmp[8:12] == '1111':
        return f'#{bin_to_hex(tmp[7::-1])}'
    if tmp[8:12] == '0111':
        return f'(IP + {bin_to_hex(tmp[7::-1]).upper().zfill(3)})', f'({sum_hex(comm, bin_to_hex(tmp[7::-1])).upper().zfill(3)})'
    if tmp[8:12] == '0011':
        return f'(SP + {bin_to_hex(tmp[7::-1])})'
    if tmp[8:12] == '1101':
        return f'-({bin_to_hex(tmp[7::-1])})'
    if tmp[8:12] == '0101':
        return f'({bin_to_hex(tmp[7::-1])})+'
    if tmp[8:12] == '0001':
        return f'({bin_to_hex(tmp[7::-1])})'


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
        print(reg, data, data_type(reg, data))


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
    try:
        pre_main()
        while True:
            keyboard.wait(HOTKEY)
            if 'БЭВМ' in pyautogui.getActiveWindowTitle():
                main()
    except KeyboardInterrupt:
        exit(0)
