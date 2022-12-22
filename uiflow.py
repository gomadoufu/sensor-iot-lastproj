from m5stack import *
from m5stack_ui import *
from uiflow import *
import json

from m5mqtt import M5mqtt
import imu
import time
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x3342a6)
tvoc_0 = unit.get(unit.TVOC, unit.PORTA)


WakeUp = None
FromCables = None
Message = None
CO2 = None
Pitch = None
Roll = None
MapData = None
JsonData = None

imu0 = imu.IMU()

label0 = M5Label('pitch', x=12, y=195, color=0xebe8bf, font=FONT_MONT_26, parent=None)
label1 = M5Label('roll', x=130, y=195, color=0xebe8bf, font=FONT_MONT_26, parent=None)
label2 = M5Label('CO2', x=250, y=196, color=0xebe8bf, font=FONT_MONT_26, parent=None)
label3 = M5Label('status', x=12, y=14, color=0xafc4fa, font=FONT_MONT_34, parent=None)
label4 = M5Label('sentencesentencese', x=12, y=80, color=0xffffff, font=FONT_MONT_14, parent=None)
label5 = M5Label('count', x=127, y=109, color=0xffffff, font=FONT_MONT_22, parent=None)
label6 = M5Label('sentencesentencesentence', x=12, y=148, color=0xffffff, font=FONT_MONT_14, parent=None)

from numbers import Number



def fun_M5_act_(topic_data):
  global WakeUp, FromCables, Message, CO2, Pitch, Roll, MapData, JsonData
  WakeUp = (WakeUp if isinstance(WakeUp, Number) else 0) + 1
  FromCables = json.loads(topic_data)
  Message = FromCables['message']
  print(Message)
  if Message == 'wakeup':
    power.setVibrationEnable(True)
    wait(0.5)
    power.setVibrationEnable(False)
    screen.set_screen_brightness(100)
    screen.set_screen_bg_color(0xff6666)
    label3.set_text_color(0xffffff)
    label3.set_text_font(FONT_MONT_48)
    label3.set_text('Wake Up!!!')
  if Message == 'goodnight':
    screen.set_screen_bg_color(0x6666cc)
    screen.set_screen_brightness(30)
    label3.set_text_color(0x9999ff)
    label3.set_text_font(FONT_MONT_34)
    label3.set_text('Good Night..')
  pass


screen.set_screen_brightness(100)
WakeUp = 0
label3.set_text('Good Night..')
label4.set_text('YOU were woken up')
label6.set_text('times, but did not wake up.')
screen.set_screen_bg_color(0x6666cc)
m5mqtt = M5mqtt('Node-RED Aedes', '192.168.0.12', 1883, '', '', 300)
m5mqtt.subscribe(str('M5-act'), fun_M5_act_)
m5mqtt.start()
while True:
  CO2 = (tvoc_0.eCO2) - 400
  Pitch = imu0.ypr[1]
  Roll = imu0.ypr[2]
  label0.set_text(str(Pitch))
  label1.set_text(str(Roll))
  label2.set_text(str(CO2))
  label5.set_text(str(WakeUp))
  MapData = {'pitch':Pitch,'roll':Roll,'co2':CO2}
  JsonData = json.dumps(MapData)
  m5mqtt.publish(str('M5-sense'), str(JsonData), 0)
  wait(1)
  wait_ms(2)

