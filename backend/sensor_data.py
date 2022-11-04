import json
from json import JSONDecodeError



class SensorData:
    def __init__(self):
        self.temp = 0.0
        self.humidity = 0
        self.pool = 0.0

    def set_temp_humidity(self, string):
        try:
            my_json = json.loads(string)
            self.temp = my_json["temp"]
            self.humidity = my_json["humidity"]
        except JSONDecodeError:
            print(f"Error decoding air/temp {string}")

    def set_pool(self, string):
        try:
            my_json = json.loads(string)
            self.pool = my_json["temp"]
        except JSONDecodeError:
            print(f"Error decoding pool {string}")

    def jsonify(self) -> str:
        try:
            string = self.__dict__
            return json.dumps(string)
        except NameError:
            print(f"Error jsonifying the object.")
