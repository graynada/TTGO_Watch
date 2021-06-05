import utime
from screens import *
from vars import *
from funcs import *

class Watch:
    def __init__(self, tft):
        self.tft = tft
        self.sta = 0x00
        self.sti = 0x00
        self.scrs = [Screen(self.tft, on = False), Home(self.tft), BT_wake(self.tft)]
        self.count = 0
        self.scr_i = HME
        self.chg_scr(self.scr_i)
        self.n_ref = (Notification('V', colour = MAG), Notification('W'), Notification('K', colour = RED))
        #self.n_act = {}
        
    def update(self):
        if self.sti:
            if self.sti & 0x03 and self.scr_i == ASLP:
                if self.sti & BTI:
                    self.chg_scr(BTW, notes = True)
                    #self.count += 85
                else:
                    self.chg_scr(HME)
                self.sti |= IHD
            else:
                self.irq()
            #self.sti = 0x00
        if self.scr_i:
            self.scr.draw()
            self.count += 1
            if self.count >= 50:
                self.chg_scr(ASLP)
        utime.sleep_ms(self.dly)
        if self.sti & IHD:
            self.sti = 0x00
        
    def chg_scr(self, scr, notes = False):
        self.scr_i = scr
        self.scr = self.scrs[scr]
        if notes:
            self.scr.ntf = self.n_ref
        self.count = 0
        self.dly = self.scr.hold
        self.scr.init()
    
    def irq(self):
        print("irq sti = {}".format(self.sti))
        self.count = 0
        self.sti |= IHD
        #self.sti = 0x00
        
    def add_irq(self, src):
        if not self.sti & src:
            self.sti |= src
            print("add_irq sti = {}".format(self.sti))
            
    def bt_rxd(self, data):
        msg = data.split(',')
        hdd = msg[0].split(':')
        if len(hdd) == 2 and hdd[0] == TYP:
            if hdd[1] == NOT and len(msg) > 1:
                rxd = {}
                for i in range(1, len(msg)):
                    item = msg[i].split(':')
                    if len(item) == 2: # and item[0] in self.n_ref.keys():
                        try:
                            #self.n_ref[item[0]].set_count(int(item[1]))
                            rxd.update({item[0] : int(item[1])})
                            #print(item)
                        except ValueError:
                            print("Value not an int")
                for n in self.n_ref:
                    count = 0
                    if n.id in rxd.keys():
                        count = rxd[n.id]
                    n.set_count(count)
                self.add_irq(BTI)
                
class Notification:
    def __init__(self, id, colour = fgc):
        self.id = id
        self.colour = colour
        self.count = 0
        self.new = False
         
    def set_count(self, count):
        self.new = self.count == count
        self.count = count
        #return new
    
    def clr_count(self):
        self.count = 0
    