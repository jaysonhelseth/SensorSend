import serial
import os
import werkzeug
from flask import Flask, request
from flask_cors import CORS, cross_origin
from backend.sensor_data import SensorData
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

air_sensor = serial.Serial(port=os.getenv("AIR_SENSOR"), baudrate=9600)
pool_sensor = serial.Serial(port=os.getenv("POOL_SENSOR"), baudrate=9600)
xbee_sender = XBeeDevice(port=os.getenv("XBEE_SENDER"), baud_rate=9600)


@app.route("/")
@cross_origin()
def display_data():
    msg = read_data()
    if msg is None:
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return ""

    send_data(msg)
    return msg


def read_data():
    global air_sensor
    global pool_sensor

    if air_sensor.closed:
        air_sensor.open()

    if pool_sensor.closed:
        pool_sensor.open()

    sensor_data = SensorData()

    try:
        air_data = air_sensor.readline()
        temp_humidity = air_data.decode("utf-8", errors="ignore").strip("\n")
        sensor_data.set_temp_humidity(temp_humidity)

        pool_data = pool_sensor.readline()
        pool_temp = pool_data.decode("utf-8", errors="ignore").strip("\n")
        sensor_data.set_pool(pool_temp)

        msg = sensor_data.jsonify()
        print(msg)
        return msg
    except:
        air_sensor.close()
        pool_sensor.close()


def send_data(payload):
    global xbee_sender

    if not xbee_sender.is_open():
        xbee_sender.open()

    try:
        xbee_sender.send_data_broadcast(payload)
    except:
        xbee_sender.close()


if __name__ == '__main__':
    app.run()
