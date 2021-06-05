from machine import Pin, TouchPad, ADC
import st7789 as st

home = Pin(0, Pin.IN)   # home button
dis = Pin(4, Pin.OUT)   # display power
bat_v = ADC(Pin(34))    # battery voltage
bat_v.atten(ADC.ATTN_11DB)
bat_cal = 1.71
t_up = TouchPad(Pin(2))
t_dn = TouchPad(Pin(12))

'''BT message constants'''
TYP = "t"  #denotes type key
NOT = "n"  #denores notification type value

''' Colours'''
BLK = st.BLACK
BLE = st.BLUE
RED = st.RED
GRN = st.GREEN
CYN = st.CYAN
MAG = st.MAGENTA
YLW = st.YELLOW
WHT = st.WHITE
MGY = 0x8410
DGY = 0x4a49
fgc = GRN #0x07E0      #foreground
bgc = BLK #0x0000      #background

'''Screen indexes'''
ASLP = const (0x00)
HME = const(0x01)
BTW = const(0x02)   # Bluetooth wake screen

''' Interrupt bits'''
HMI = const(0x01)   # Home btn interrupt
BTI = const(0x02)   # Bluetooth interupt
UPI = const(0x04)   # Up touch interrupt
DWI = const(0x08)   # Down touch interrupt
IHD = const(0x80)   # Interrupt set

'''Status bits'''
WFO = const(0x20)   # WiFi on
BTO = const(0x40)   # Bluetooth on
SLP = const(0x80)   # Watch asleep
sts = 0x00
sta = 0x00          # Status register A
sti = 0x00          # Interrupt status register

'''Text justification constants. First char is horizontal justification, second vertical'''
LT = const(0x00)    # Justfy left and top
LC = const(0x01)    # Justty left and centre
CC = const(0x11)    # Justify centre and centre

'''Array of days of the week indexed to utime value'''
DAY = ["Mon",
       "Tue",
       "Wed",
       "Thu",
       "Fri",
       "Sat",
       "Sun"
       ]

'''Array of months of the year indexed to utime value'''
MONTH = ["",
         "Jan",
         "Feb",
         "Mar",
         "Apr",
         "May",
         "Jun",
         "Jul",
         "Aug",
         "Sep",
         "Oct",
         "Nov",
         "Dec"
         ]

''' Binary image of outline of the battery'''
bat_out = (
    b'\x1c\x0f'
    b'\x02\x00\x16\x02'
    b'\x02\x0d\x16\x02'
    b'\x00\x02\x02\x0b'
    b'\x18\x02\x02\x0b'
    b'\x1a\x05\x02\x05'
    b'\x01\x01\x02\x02'
    b'\x17\x01\x02\x02'
    b'\x17\x0c\x02\x02'
    b'\x01\x0c\x02\x02'
)

''' Binary image of an inside blob of battery charged capacity'''
bat_in = (
    b'\x06\x08'
    b'\x00\x01\x06\x07'
    b'\x01\x00\x04\x01'
    b'\x01\x08\x04\x01'
)

''' Binary image the battery charging symbol'''
bat_chg = (
    b'\x14\x08'
    b'\x09\x01\x01\x04'
    b'\x0a\x03\x01\x04'
    b'\x08\x02\x01\x02'
    b'\x0b\x04\x01\x02'
    b'\x06\x03\x02\x02'
    b'\x0c\x03\x02\x02'
    b'\x04\x04\x02\x01'
    b'\x0e\x03\x02\x01'
)