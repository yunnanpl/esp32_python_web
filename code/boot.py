### boot.py

# Done by Dr.JJ
# https://github.com/yunnanpl/esp32_python_web

from secret_cfg import *
from functions import *

from machine import Pin, DAC, PWM, ADC
import machine
machine.freq( config['freq'] )
import network
import ntptime
import time
import random
import _thread #experimental
import socket
import binascii

import umqtt.simple

import gc
gc.collect()

### other useful modules
#import sys
#import os
#import esp
#esp.osdebug(None)

### definition for leds
# defined early, for signaling
# 26, 25 are dac
# 35, 34 are only input

leds = {}
ledsp = {}
for iii in [13,12,14,27,33]:
  leds[iii] = Pin(iii, Pin.OUT)
  ledsp[iii] = PWM( leds[iii] )
  ledsp[iii].freq(1000)
  ledsp[iii].duty( 0 )
inps = {}
inpv = {}
for iii in [21,22,23]:
  inps[iii] = Pin(iii, Pin.IN, Pin.PULL_UP)
  inpv[iii] = inps[iii].value()

ina35 = ADC( Pin(35) )
inp34 = Pin(34, Pin.IN)

### log file open
if config['log_boots'] == 1:
  aa = open('log.txt', 'a')
  aa.write('\nbooting -> ')

### conenct to network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect( config['wifi_name'], binascii.a2b_base64( config['wifi_pass'] ) )

# if not connected then one led is blinking
# a thread ?
# no thread at boot time, as other services are waiting
while station.isconnected() == False:
  ledsp[27].duty( 0 )
  time.sleep(0.2)
  ledsp[27].duty( 10 )
  time.sleep(0.2)

print('LOG Connection successful')
print('LOG '+ str( station.ifconfig() ))
###

### getting ntp time
ntptime.host = config['ntp_host']
ntptime.settime()
print('LOG NTP time set')

### mqtt definition
# only if you have mqtt server
#mqtts = umqtt.simple.MQTTClient('esp_test', config['mqtt_host'] )

### starting webrepl
import webrepl
webrepl.start()

### booting done, logging
# if boot is loaded correctly then second led
ledsp[33].duty( 10 )

# define uptime
uptime = "{0:04d}-{1:02d}-{2:02d}".format( *time.localtime() ) + " {3:02d}:{4:02d}:{5:02d}".format( *time.localtime() ) + ''
# if all is done and led is on, then log successfull booting

if config['log_boots'] == 1:
  # this can be removed to save the memory life
  aa.write( "booted on " + uptime + '' )
  aa.close()
  # cutting down to 10 lines
  bb = open('log.txt', 'r')
  bbread = bb.readlines()
  bb.close()
  cc = open('log.txt', 'w')
  cc.write( ''.join( bbread[-10:] ) )
  cc.close()

# clean up the config variable, so that it is not available
config = ''
del config
### BOOTED
### end