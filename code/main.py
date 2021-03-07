### main.py

### webpages code
header_ok = """HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

"""

header_see = """HTTP/1.1 303 See Other
Location: /

"""

def web_page():
  #out_dac = request.split('dac=')[1]
  out_time = "{3:02d}:{4:02d}:{5:02d}".format( *time.localtime() )
  out_date = "{0:04d}-{1:02d}-{2:02d}".format( *time.localtime() )

  html_b = ""
  for led in ledsp.items():
    #led_val = int( led[1].value() )
    led_val = bool( led[1].duty() )
    iii = str( led[0] )
    #print(iii, led_val)
    if led_val is False:
      html_b = html_b + """<p><a href="/?led"""+ iii +"""=on"><button class="button">ON """+ iii +"""</button></a></p>"""
    elif led_val is True:
      html_b = html_b + """<p><a href="/?led"""+ iii +"""=off"><button class="button button2">OFF """+ iii +"""</button></a></p>"""
  del iii
  #print(html_b)

  html_in = ""
  for inp in inps.items():
    jjj = str( inp[0] )
    html_in = html_in + "<p>" + jjj + "-" + str( inp[1].value() ) + "</p>"
  #print(html_in)
  html = """<html><head>
<title>ESP Web Server 5</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}
</style>
</head>
<body>
<h1>ESP Web Server</h1>
<p>GPIO state</p>""" + html_b +"""
<p>Time:""" + out_date + """ """ + out_time + """</p>
<p>Boot:""" + uptime + """</p>
<p>""" + html_in + """</p>
</body>
</html>"""
  return html

### creating sockets etc
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#SO_REUSEPORT
# from 300 to 60
s.settimeout(60)
#s.setblocking(1) # has to be blocking if using accept
s.bind(('', 80))
s.listen(2)
#print( _thread.get_ident() )

### webpage socket loop
def loop_web():
  #print( _thread.get_ident() )
  while keep_loop:
    # try to listen for connection
    try:
      if gc.mem_free() < 80000: # 92k is good
        gc.collect()
        #print('LOG g cleaning', str( gc.mem_free() ) )
      conn, addr = s.accept()
      # set to 3 seconds
      conn.settimeout(5)
      # request placed in try, just in case
      request = conn.recv(1024)
      request = str(request[0:64]) # shorten the request to cut the headers away
      # this has to work, no try needed
      if request.find('/?led') == 6:
        if request.find('=on') == 13:
          kkk = int( request[11:13] )
          led_on( ledsp[kkk], intensity )
        elif request.find('=off') == 13:
          kkk = int( request[11:13] )
          led_off( ledsp[kkk] )
        # if the request is sent, then redirect to clean page
        conn.sendall( header_see ) # do not close, much faster this way
        conn.close() # edge and iphone need this after redirect, otherwise they kill esp32
        #print('LOG redirect sent')
        continue
      conn.sendall( header_ok + web_page() )
      conn.close()
      #print('LOG page sent')
    # except with error value does not work as timeout is special
    #except (TypeError, ValueError) as e:
    #  # collecting both timeout, and problems with sendall
    #  print('LOG exception', e)
    except:
      # this is critical, as timeout error is special
      #print('LOG accept timeouted or other error')
      pass
    #finally:
    #  time.sleep(0.1) # keep awake

### creating wifi and activity check
def loop_wifi():
  while keep_loop:
    time.sleep(10)
    led_tog( ledsp[33], intensity )
    if station.isconnected() == False:
      led_off( ledsp[27] )
    else:
      led_on( ledsp[27], intensity )

### callback
def cb_mqtt(topic, msg):
  print( topic )
  print( msg )

### callback
def cb_btn(ppp):
  #time.sleep(0.1)
  # compare if changed
  if inpv[ int( str( ppp )[4:6] ) ] == ppp.value():
    # this is debouncing
    pass
  elif ppp.value() == 0:
    # press
    #ppp = int( str( ppp )[4:6] )
    #print('pin', str( ppp ), str( ppp.value() ) )
    if str(ppp) == "Pin(21)":
      led_tog( ledsp[12] )
    if str(ppp) == "Pin(22)":
      led_tog( ledsp[13] )
    if str(ppp) == "Pin(23)":
      led_tog( ledsp[14] )
  # write new value
  inpv[ int( str( ppp )[4:6] ) ] = ppp.value()

### mqtt callback
#mqtts.set_callback( cb_mqtt )
#mqtts.connect()
#mqtts.subscribe( "/aaaa/aaaa" )

### creating interrupts
inps[21].irq( trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=cb_btn )
inps[22].irq( trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=cb_btn )
inps[23].irq( trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=cb_btn )

### starting thread
loopwifithread = _thread.start_new_thread(loop_wifi, ())
loopwebthread = _thread.start_new_thread(loop_web, ())

### end