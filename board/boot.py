from machine import Pin
modepin = Pin(14, Pin.IN, Pin.PULL_DOWN)



if modepin.value():
	wifi_ssid = "izel"
	wifi_passwd = "98761234"

	import network
	import machine
	import time

	sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
	sta_if.connect(wifi_ssid, wifi_passwd)
	time.sleep(6)
	sta_if.ifconfig()
	if sta_if.isconnected():
	    ip = network.WLAN(network.STA_IF).ifconfig()[0]
	    print("Connected to %s - ip: %s" % (wifi_ssid, ip))
	    network.ftp.start(user="micro", password="python", buffsize=1024, timeout=300)
	    network.telnet.start(user="micro", password="python", timeout=300)
