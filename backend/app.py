import serial
import os
import werkzeug
import sys
from serial import SerialException
from flask import Flask, request
from flask_cors import CORS, cross_origin
from sensor_data import SensorData

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

locked = False


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

    # send_data(msg)
    return msg


def read_data():
    global locked
    
    air_sensor = serial.Serial(port=os.getenv("AIR_SENSOR"), baudrate=9600)
    pool_sensor = serial.Serial(port=os.getenv("POOL_SENSOR"), baudrate=9600)
    
    if locked is True:
        print("The read thread is locked.")
        return f'{{ "msg": "locked" }}'


    locked = True

    if air_sensor.closed:
        air_sensor.open()

    if pool_sensor.closed:
        pool_sensor.open()

    sensor_data = SensorData()

    try:
        air_data = b''
        while len(air_data) < 1:
            air_data = air_sensor.read_until("\n".encode())

        temp_humidity = air_data.decode("utf-8", errors="ignore").strip("\n")
        sensor_data.set_temp_humidity(temp_humidity)

        pool_data = b''
        while len(pool_data) < 1:
            pool_data = pool_sensor.read_until("\n".encode())

        pool_temp = pool_data.decode("utf-8", errors="ignore").strip("\n")
        sensor_data.set_pool(pool_temp)

        msg = sensor_data.jsonify()
        print(msg)
        locked = False

        air_sensor.close()
        pool_sensor.close()
        return msg
        
    except SerialException as serialEx:
        print(serialEx.message)
        air_sensor.close()
        pool_sensor.close()
        locked = False
        return f'{{ "msg": "{serialEx.message}" }}'
    except:
        print("Unexpected error:", sys.exc_info()[0])
        air_sensor.close()
        pool_sensor.close()
        locked = False
        return f'{{ "msg": "{sys.exc_info()[0]}" }}'

if __name__ == '__main__':
    app.run()
