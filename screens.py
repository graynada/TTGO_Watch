''' Classes and functions to draw the Screens '''
import utime
import esp32
from vars import *
from funcs import *

def draw_bat(tft, bl, x = 200, y = 0, w = 40, h = 25):
    #bl = get_bat_v() // 100
    xb = x + (w - bat_out[0]) // 2
    yb = y + (h - bat_out[1]) // 2
    #print("battery level {}".format(bl))
    if bl < 1:
        tft_draw(tft, x, y, bat_out, justify = CC, w = w, h = h, fg = RED)
    else:
        tft_draw(tft, x, y, bat_out, justify = CC, w = w, h = h)
        if bl > 3:
            tft_draw(tft, xb + 3, yb + 3, bat_chg)
        else:
            for i in range (bl):
                if bl > i:
                    tft_draw(tft, xb + 3 + i * 7, yb + 3, bat_in, transparent = True)

class Screen:
    def __init__(self, tft, hold = 200, fg = fgc, bg = bgc, on = True):
        self.tft = tft
        self.hold = hold
        self.fg = fg
        self.bg = bg
        if on:
            self.on = 1
        else:
            self.on = 0
        self.ntf = {}
    
    def init(self):
        global dis
        self.tft.fill(self.bg)
        dis.value(self.on)
        
    def draw(self):
        pass
    
    def up(self):
        pass
    
    def down(self):
        pass
    
    def irq(self, src):
        print("Screen.irq({})".format(src))
        

class Home(Screen):
    def init(self):
        super().init()
        self.ds = 61
        self.dm = 61
        self.dh = 25
        self.dd = 367
        self.db = 5
        
    #@timed_function
    def draw(self):
        t_now = utime.localtime()
        w = write
        tft = self.tft
        if not self.ds == t_now[5]:
            self.ds = t_now[5]
            w(tft, 200, 25, "{:02d}".format(self.ds), w = 40, h = 25, justify = CC, scale = 2)
            w(tft, 0, 0, "W", w = 40, h = 25, justify = CC, scale = 2, fg = DGY)
            w(tft, 0, 25, "B", w = 40, h = 25, justify = CC, scale = 2, fg = DGY)
            if self.ds % 10 == 0 or self.db == 5:
                db_n = get_bat_lvl()
                if not self.db == db_n:
                    self.db = db_n
                    draw_bat(tft, db_n)
        if not self.dm == t_now[4]:
            self.dm = t_now[4]
            w(tft, 125, 0, "{:02d}".format(self.dm), w = 75, h = 50, justify = CC, scale = 5)
        if not self.dh == t_now[3]:
            self.dh = t_now[3]
            w(tft, 40, 0, "{:02d}".format(self.dh), w = 75, h = 50, justify = CC, scale = 5)
        if not self.dd == t_now[7]:
            self.dd = t_now[7]
            w(tft, 0, 50, "{} {} {} {}".format(DAY[t_now[6]],t_now[2],MONTH[t_now[1]],t_now[0]), w = 240, h = 20, justify = CC, scale = 2)

class Head(Home):
    def init(self):
        super().init()
        
    def draw(self):
        t_now = utime.localtime()
        if not self.ds == t_now[5]:
            self.ds = t_now[5]
            if self.ds % 2:
                write(self.tft, 165, 0, ":", w = 0, h = 25, justify = CC, scale = 2)
            else:
                write(self.tft, 165, 0, ":", w = 0, h = 25, justify = CC, scale = 2, fg = bgc)
        if not self.dm == t_now[4]:
            self.dm = t_now[4]
            write(self.tft, 167, 0, "{:02d}".format(self.dm), w = 28, h = 25, justify = CC, scale = 2)
            db = get_bat_lvl()
            if not self.db == db:
                self.db = db
                draw_bat(self.tft, db)
        if not self.dh == t_now[3]:
            self.dh = t_now[3]
            write(self.tft, 135, 0, "{:02d}".format(self.dh), w = 28, h = 25, justify = CC, scale = 2)

class BT_wake(Head):
    def init(self):
        super().init()
        for n in self.ntf:
            print("{}:{}".format(n.id, n.count))
            
    def draw(self):
        super().draw()
