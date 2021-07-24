# SensorSend

This code will listen for serial device updates and send them via the Xbee (Zigbee) 
protocol to all Xbee connected devices. At the same time the data will be sent
through a websocket to the device that is hosting this code. The websocket will
prevent the data locally on a screen via a locally hosted web page.