# SensorSend

This code will listen for serial device updates and send them via the Xbee (Zigbee) 
protocol to all Xbee connected devices. At the same time the data will be sent
through a websocket to the device that is hosting this code. The websocket will
prevent the data locally on a screen via a locally hosted web page.

## Helpful Device Configuration
On linux in `/etc/udev/rules.d` make a 99-usb-serial.rules or 100-usb-serial.rules file to be able to figure out your usb serial devices so you don't have to guess which one is plugged into `/dev/ttyUSB0`. In the file put this data:
```
SUBSYSTEM=="tty",
SUBSYSTEMS=="usb",
DRIVERS=="usb",
SYMLINK+="device_%s{serial}"
```
Then in the code you can reference by serial number instead!