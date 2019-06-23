
The Micropython firmware for Talktopus is MicroPython_ESP32_psRAM_LoBo https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/
This distro contains the following services prebuilt:

FTP Server
Telnet Server
Mqtt client
mDNS Server

Docmentation: https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki

to build the firmware:
follow: https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/build
enable MQTT and Websockets at BUILD.sh menuconfig


before you flush it, do an erase:

esptool.py --chip esp32 -p /dev/ttyUSB0 erase_flash

once flashed:

(you'll need to manually reset the board)

use picoterm to connect to the REPL

 picocom /dev/ttyUSB0 -b 115200

copy and paste into  REPL to enable ftp

-------
wifi_ssid = "xxxx"
wifi_passwd = "xxxxxx"

import network
import machine
import time

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.connect(wifi_ssid, wifi_passwd)
time.sleep(6)
sta_if.ifconfig()

network.ftp.start(user="micro", password="python", buffsize=1024, timeout=300)
-------


transfer boot.py to activate Telnet and FTP
With Curl:

curl -B -s -S -T boot.py ftp://micro:python@192.168.1.XXX/flash/


### LOLIN D32 ####

BUILD.sh flash fails
I managed to flush the binaries as follows:
>BUILD.sh all
>cd MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build
>esptool.py --chip esp32 -p /dev/ttyUSB0 erase_flash
>esptool.py --chip esp32 -p /dev/ttyUSB0  write_flash -z 0x1000 bootloader/bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin




 
