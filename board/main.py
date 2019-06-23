from machine import Pin, PWM, Timer
from time import ticks_ms, sleep_ms
from sys import exit
#Buttons
UP_PIN = 13
DW_PIN = 14
ST_PIN = 12
#Stepper
DIR_PIN = 21
STP_PIN = 22
#LED
LED_PIN = 32

#globals
SET_MODE = 'operational'
MEASURING = False
START_MEASURE = 0

def up_action(pin, value):
    if value:
        print('UP button pressed')
        if motor.position < 2 and motor.started_rising == 0:
            motor.started_rising = ticks_ms() # store time it began to rise
        else:
            time_left = motor.song_length - (ticks_ms() - motor.started_rising)
            motor.update_freq(time_left)
        motor.set_direction(1)
        motor.start()
    else:
        print('UP button released')
        print('Motor Position: %s' % motor.position)
        motor.stop()

def dw_action(pin, value):
    global MEASURING, START_MEASURE
    print('DOWN button pressed', value)
    if value:
        if SET_MODE == 'length':
            # measuring length of song
            if not MEASURING:
                MEASURING = True
                START_MEASURE = ticks_ms()
                print('Starting song length measurment')
                return
            if MEASURING:
                motor.song_length = ticks_ms() - START_MEASURE
                print('End of song measurement - length:%s ms' % motor.song_length)
                MEASURING = False
                return

        # moving the motor
        motor.freq = motor.default_freq # when down use always default speed
        motor.set_direction(0)
        motor.start()
    else:
        print('DOWN button released')
        print('Motor Position: %s' % motor.position)
        if SET_MODE != 'operational':
            motor.stop()

def st_action(pin, value):
    global SET_MODE
    if value:
        print('Setting mode button pressed')
        if SET_MODE == 'operational':
            motor.freq = motor.default_freq
            motor.store_position = motor.max_position
            motor.max_position = 1000000 #infinite
            motor.position = 1
            SET_MODE = 'height'
            led.blink()
            return

        if SET_MODE == 'height':
            if motor.position < motor.min_store_position:
                motor.max_position = motor.store_position
            else:
                motor.max_position = motor.position
            fp=open('max_position', 'w')
            fp.write(str(motor.max_position))
            fp.flush()
            fp.close()
            print('Pole height stored')
            motor.set_direction(0)
            motor.start()
            SET_MODE = 'length'
            motor.store_song_length = motor.song_length
            led.blink(4)
            return

        if SET_MODE == 'length':
            if motor.song_length > motor.min_song_length:
                fp = open('song_length', 'w')
                fp.write(str(motor.song_length))
                fp.flush()
                fp.close()
                print('Song length stored')
            else:
                motor.song_length = motor.store_song_length
            motor.update_freq()
            SET_MODE = 'operational'
            led.on()
    else:
        print('Setting mode button released', SET_MODE, value )

class Stepper:
    def __init__(self, dir_pin, stp_pin):
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.stp_pin = Pin(stp_pin)
        self.start_time = 0
        self.end_time = 0
        self.stp_per_rev = 800
        self.position = 1
        self.max_position = 3200
        self.timer = Timer(0)
        self.moving = False
        self.up_compensation = 20
        self.down_compensation = 26
        self.default_song_length = 82302 # SG National Anthem
        self.song_length = self.default_song_length
        self.min_song_length = 20000 # 20sec
        self.store_song_length = 0
        self.default_freq = 3000
        self.max_freq = 5000
        self.min_freq = 100
        self.freq = self.get_freq(self.song_length)
        self.store_position = 0
        self.min_store_position = 4000 # 5 revs
        self.started_rising = 0 # stores the time the flag started rising

    def get_period(self, steps):
        return abs(int(round(steps/self.freq * 1000)))

    def get_freq(self, length):
        freq = int((self.max_position - self.position)/(length/1000))
        if freq > self.max_freq: freq = self.max_freq
        if freq < self.min_freq: freq = self.min_freq
        return freq

    def update_freq(self, length=None):
        if not length: length = self.song_length
        self.freq = self.get_freq(length)
        print('new frequency: %s' % self.freq)

    def start(self):
        if self.direction and self.position >= self.max_position:return
        if not self.direction and self.position <= 1: return
        self.moving = True
        if self.direction:
            period = self.get_period(self.max_position - self.position)
        else:
            period = self.get_period(self.position)
        if period > 0:
            self.start_time = ticks_ms()
            self.motor = PWM(self.stp_pin, freq=self.freq, duty=50)
            self.timer.init(mode=Timer.ONE_SHOT, period=period, callback=self.stop)

    def stop(self, arg=None):
        if not self.moving: return
        self.motor.deinit()
        self.stop_time = ticks_ms()
        self.moving = False
        self.timer.deinit()
        if self.direction:
            self.position += int(self.freq/1000.0  * (self.stop_time - self.start_time))
            self.position -= self.up_compensation
        else:
            self.position -= int(self.freq/1000.0  * (self.stop_time - self.start_time))
            self.position += self.down_compensation

            if self.started_rising and SET_MODE=='operational':
                self.position = 0
                self.started_rising = 0
                self.update_freq()

    def set_direction(self, dir):
        self.dir_pin.value(dir)
        self.direction = dir

class Switch:
    def __init__(self, pin, callback):
        self.last = False
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN,
                       trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                       handler=self.action,
                       debounce=250000)
        self.callback = callback

    def action(self, pin):
        value = self.pin.value()
        if value != self.last:
            self.callback(pin, value)
            self.last = value

class Led:
    def __init__(self, pin):
        self.pin = Pin(pin)
        self.led = PWM(self.pin, freq=1, duty=0)

    def blink(self, freq=1, duty=50):
        self.led.init(freq=freq, duty=duty)

    def on(self):
        self.led.init(freq=1, duty=100)

    def off(self):
        self.led.deinit()

up = Switch(UP_PIN, up_action)
dw = Switch(DW_PIN, dw_action)
st = Switch(ST_PIN, st_action)

led = Led(LED_PIN)
led.on()

motor = Stepper(DIR_PIN, STP_PIN)
max_position = open('max_position').read()
song_length = open('song_length').read()
print('max_position:', max_position)
print('song_length:', song_length)

if max_position:
    motor.max_position = int(str(max_position))

if song_length:
    motor.song_length = int(str(song_length))

# set the new motor speed
motor.update_freq()
