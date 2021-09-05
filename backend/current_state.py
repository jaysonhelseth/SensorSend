import json
import time
import serial
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress


class State:
    def __init__(self):
        self.msg = None
        self.do_run_thread = True
        self.serial = None
        try:
            self.serial = serial.Serial(
                port="/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0", 
                baudrate=9600)
            
            self.xbee = XBeeDevice(
                port="/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D309RJOH-if00-port0",
                baud_rate=9600)
            self.xbee.open()
        except:
            pass

    def update_state(self):
        while self.do_run_thread:
            try:
                self.check_status()
                data = self.serial.readline()
                
                msg = data.decode("utf-8", errors="ignore").strip("\n")
                self.xbee.send_data_broadcast(msg)
                self.msg = msg

            except:
                if self.serial is not None:
                    self.serial.close()
                self.msg = "Error. There was an error finding a serial device."

            time.sleep(2)
        self.serial.close()

    def check_status(self):
        if self.serial is None:
            try:
                self.serial = serial.Serial(port="/dev/tty.usbserial-120", baudrate=9600)
            except:
                pass

        if not self.serial.is_open:
            self.serial.open()


    def jsonify(self):
        if self.msg is None:
            data = {"msg": "Error reading from serial device."}
            return json.dumps(data)

        if self.msg.startswith("Error"):
            data = {"msg": self.msg}
            return json.dumps(data)

        return self.msg
