### functions.py

#while 1:
#  time.sleep(0.2)
#  ledtoggle( random.choice( list(leds.values()) ) )
def led_on( leda, intensity=10 ):
  leda.duty( intensity )

def led_off(leda):
  leda.duty( 0 )

def flicker():
  while 1:
    time.sleep(0.01)
    random.choice( list(ledsp.values() ) ).duty(  round(random.random()*200) )

###
def logp():
  bbbb = open('log.txt', 'r')
  #for jjj in bbbb:
  #  print(jjj)
  #print( bbbb.read() )
  bbbb.close()

###
def logd():
  bbbb = open('log.txt', 'w')
  bbbb.write('')
  bbbb.close()

def led_tog(leda, intensity=10):
  if leda.__class__.__name__ is 'PWM':
    leda.duty( int( not leda.duty() ) * intensity )
  elif leda.__class__.__name__ is 'Pin':
    leda.value( not leda.value() )
  else:
    pass
    #print('no type')

### END