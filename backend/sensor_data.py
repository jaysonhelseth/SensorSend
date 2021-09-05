import json


class SensorData:
    def __init__(self):
        self.temp = 0.0
        self.humidity = 0
        self.pool = 0.0

    def set_temp_humidity(self, string):
        my_json = json.loads(string)
        self.temp = my_json["temp"]
        self.humidity = my_json["humidity"]

    def jsonify(self) -> str:
        string = self.__dict__
        return json.dumps(string)
