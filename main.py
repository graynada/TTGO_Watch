from machine import Pin, SPI, RTC, freq
import  time, math, network, utime
import st7789, esp32
from watch import Watch
from vars import *
from screens import *
from ntptime import settime
from bt import *
from protect import *

wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, ssid_password)

tft = st7789.ST7789(
    SPI(2, baudrate=30000000, polarity=1, sck=Pin(18), mosi=Pin(19)),
    135,
    240,
    cs=Pin(5, Pin.OUT),
    reset=dis,
    dc=Pin(16, Pin.OUT),
    rotation=1)
tft.init()

watch = Watch(tft)

def home_int(pin):
    interrupt(HMI)
        
def up_int(pin):
    print("up")

home.irq(trigger = Pin.IRQ_FALLING, handler = home_int)

while not wifi.isconnected():
    utime.sleep_ms(200)
print(wifi.ifconfig()[0])

rtc = RTC()
if rtc.datetime()[0] < 2020:
    settime()
    print("RTC set {}".format(utime.localtime()))

freq(80000000)

def interrupt(src):
    global watch
    watch.add_irq(src)

ble = bluetooth.BLE()
uart = BLEUART(ble)

def on_rx():
    global watch
    watch.bt_rxd(uart.read().decode().strip())

uart.irq(handler=on_rx)

''' Main loop '''
while True:
    if t_up.read() < 550:
        watch.add_irq(UPI)
        print("t_up value = {}".format(t_up.read()))
    if t_dn.read() < 550:
        watch.add_irq(DWI)
        print("t_dn value = {}".format(t_dn.read()))
    watch.update()
      