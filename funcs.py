from machine import ADC
from vars import *
import utime

#@timed_function
def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

def get_bat_v():
    lvls = 0
    for i in range (0, 5):
        lvls += bat_v.read()
    return int((lvls // 5) * bat_cal)

def get_bat_lvl():
    bat_lvl = get_bat_v() // 100 - 36
    if bat_lvl < 0:
        bat_lvl = 0
    if bat_lvl > 3:
        bat_lvl = 4
    return bat_lvl

#@timed_function
def write(tft, x, y, text, justify = LT, w = 0, h = 0, transparent = False, fg = fgc, bg = bgc, margin = 1, scale = 1):
    chars = {
        "0" : b'\x57\x10\x31\x01\x15\x41\x15\x16\x31',
        "1" : b'\x57\x20\x16\x11\x11\x16\x31',
        "2" : b'\x57\x10\x31\x01\x11\x41\x12\x33\x11\x24\x11\x15\x11\x06\x51',
        "3" : b'\x57\x10\x31\x01\x11\x41\x12\x23\x21\x44\x12\x05\x11\x16\x31',
        "4" : b'\x57\x30\x17\x21\x11\x12\x11\x03\x11\x04\x51',
        "5" : b'\x57\x00\x51\x01\x12\x12\x31\x43\x13\x05\x11\x16\x31',
        "6" : b'\x57\x30\x11\x21\x11\x12\x11\x03\x41\x04\x12\x44\x12\x16\x31',
        "7" : b'\x57\x00\x51\x41\x12\x33\x11\x24\x11\x15\x11\x06\x11',
        "8" : b'\x57\x10\x31\x01\x12\x41\x12\x13\x31\x04\x12\x44\x12\x16\x31',
        "9" : b'\x57\x10\x31\x01\x12\x41\x12\x13\x41\x34\x11\x25\x11\x16\x11',
        ":" : b'\x17\x02\x11\x05\x11',
        " " : b'\x47\x00\x00',
        "a" : b'\x47\x12\x21\x33\x14\x14\x21\05\x11\x16\x21',
        "b" : b'\x47\x00\x17\x12\x21\x33\x13\x16\x21',
        "c" : b'\x47\x12\x21\x03\x13\x16\x21\x33\x11\x35\x11',
        "d" : b'\x47\x30\x17\x12\x21\x03\x13\x16\x21',
        "e" : b'\x47\x12\x21\x03\x13\x33\x11\x14\x21\x16\x21',
        "g" : b'\x49\x03\x12\x12\x21\x33\x15\x15\x21\x07\x11\x18\x21',
        "h" : b'\x47\x00\x17\x12\x21\x33\x14',
        "i" : b'\x17\x01\x11\x03\x14',
        "l" : b'\x27\x00\x16\x16\x11',
        "n" : b'\x47\x02\x15\x12\x21\x33\x14',
        "o" : b'\x47\x12\x21\x03\x13\x33\x13\x16\x21',
        "p" : b'\x49\x02\x17\x12\x21\x33\x13\x16\x21',
        "r" : b'\x47\x02\x15\x13\x11\x22\x21',
        "t" : b'\x37\x00\x16\x12\x21\x16\x21',
        "u" : b'\x47\x02\x14\x16\x31\x32\x14',
        "v" : b'\x47\x02\x13\x32\x13\x15\x22',
        "y" : b'\x49\x02\x13\x32\x16\x15\x21\x07\x11\x18\x21',
        "A" : b'\x57\x20\x11\x11\x11\x31\x11\x02\x15\x42\x15\x14\x31',
        "B" : b'\x57\x00\x17\x10\x31\x13\x31\x16\x31\x41\x12\x44\x12',
        "D" : b'\x57\x00\x17\x10\x31\x41\x15\x16\x31',
        "F" : b'\x57\x00\x17\x10\x41\x13\x31',
        "J" : b'\x57\x00\x51\x31\x15\x05\x11\x16\x21',
        "M" : b'\x57\x00\x17\x40\x17\x11\x11\x31\x11\x22\x12',
        "N" : b'\x57\x00\x17\x40\x17\x11\x12\x22\x13\x34\x12',
        "O" : b'\x57\x10\x31\x01\x15\x41\x15\x16\x31',
        "P" : b'\x57\x00\x17\x10\x31\x13\x31\x41\x12',
        "S" : b'\x57\x10\x31\x01\x12\x13\x31\x44\x12\x16\x31',
        "T" : b'\x57\x00\x51\x21\x16',
        "W" : b'\x57\x00\x16\x40\x16\x23\x13\x16\x11\x36\x11'
        }
    tw = 0 #text width
    th = 0 #text height
    ww = w #window width
    wh = h #window height
    xc = x #start x for next character
    yc = y
    #dr = tft.fill_rect
    #t = time.ticks_ms()
    for c in text:
        tw += (chars[c][0] >> 4) + margin
        ch = (chars[c][0] & 0x0f) * scale
        if ch > th:
            th = ch
    tw = (tw - margin) * scale
    if tw > ww:
        ww = tw
    if th > wh:
        wh = th
    if justify >> 4 == 0x01:
        xc = x + (ww - tw) // 2
    if justify & 0x0f == 0x01:
        yc = y + (wh - th) // 2
    #print("x:{:d}, y:{:d}, xc:{:d}, yc:{:d}, tw:{:d}, th:{:d}, ww:{:d}, wh:{:d}".format(x,y,xc,yc,tw,th,ww,wh))
    tft.fill_rect(x, y, ww, wh, bg)
    for c in text:
        cb = memoryview(chars[c])  #char bytearray 
        w = (cb[0] >> 4) * scale   #width
        h = (cb[0] & 0x0f) * scale   #height
        #if not transparent:
            #tft.rect(xc, yc, w, h, color = bg, fillcolor = bg)
        for i in range(1, len(cb), 2):
            px = xc + (cb[i] >> 4) * scale
            py = yc + (cb[i] & 0x0f) * scale
            pw = (cb[i + 1] >> 4) * scale
            ph = (cb[i + 1] & 0x0f) * scale
            tft.fill_rect(px, py, pw, ph, fg)
        xc += w + (margin * scale)
    #t = (time.ticks_ms() - t)
    #print("Time taken {:d}ms".format(t))

def tft_draw(tft, x, y, img, w = 0, h = 0, justify = LT, transparent = False, fg = fgc, bg = bgc):
    ib = img     #local copy of image bytes
    xs = x       #x start posn
    ys = y       #y start posn
    ww = min(w, ib[0])
    wh = min(h, ib[1])
    if justify >> 4 == 0x01:
        xs += (w - ib[0]) // 2
    if justify & 0x0f == 0x01:
        ys += (h - ib[1]) // 2
    if not transparent:
        tft.fill_rect(xs, ys, ww, wh, bg)
        #print("xs: {}, ys: {}, ww: {}, wh: {}".format(xs, ys, ww, wh))
    for i in range(2, len(ib), 4):
        bx = xs + ib[i]
        by = ys + ib[i + 1]
        bw = ib[i + 2]
        bh = ib[i + 3]
        tft.fill_rect(bx, by, bw, bh, fg)
