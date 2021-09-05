import serial
import os
from flask import Flask
from flask_cors import CORS, cross_origin
from backend.sensor_data import SensorData

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
air_sensor = serial.Serial(port=os.getenv("AIR_SENSOR"), baudrate=9600)
sensor_data = SensorData()


@app.route("/")
@cross_origin()
def get_data():
    return read_data()


def read_data():
    global air_sensor
    global sensor_data

    if air_sensor.closed:
        air_sensor.open()

    data = air_sensor.readline()
    temp_humidity = data.decode("utf-8").strip("\n")
    sensor_data.set_temp_humidity(temp_humidity)

    msg = sensor_data.jsonify()
    print(msg)
    return msg


if __name__ == '__main__':
    app.run()
