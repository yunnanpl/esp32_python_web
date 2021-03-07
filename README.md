# esp32_python_web
As the name says, it is about simple, stable web server on esp32 using micropython. This is a base for most other projects.<br/>
Unfortunately it required a lot of testing, to go from the basic examples to a stable working web server.<br/>
Now it easily survives days, multiple request from multiple clients, etc.<br/>

Testing included:<br/>
= timeout errors<br/>
= network errors<br/>
= iphone killing sockets (yes...)<br/>
= sending errors and more

This version includes:<br/>
= web server running in thread<br/>
= signal led showing connected wifi and running system in thread<br/>
= interrupts for buttons<br/>
= some leds as PWM for lower intensity (I connected most of leds directly, without resistor)

Idea is:<br/>
= use this base for other projects such as:
= sensors (different MQ sensors and temperature sensors)<br/>
  mainly natural gas and carbon monooxide for gas heater safety<br/>
= mqtt connection<br/>
= bluetooth eq3 thermostats control<br/>
= bluetooth scanner for presence testing

Created and tested on<br/>
= micropython, esp32-idf4-20201114-unstable-v1.13-173-g61d1e4b01.bin<br/>
= esp32-wroom-32 (from AZ-Delivery)<br/>
= some leds and buttons<br/>
= sensors

Helpful projects<br/>
https://github.com/leech001/MQ9<br/>
https://github.com/kartun83/micropython-MQ

Page layout and basics from<br/>
https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
