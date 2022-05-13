try:
    import os
    import sys
    import datetime
    import time
    import boto3
    import Adafruit_DHT
    import threading
    from datetime import datetime
    print("All Modules Loaded ...... ")
except Exception as e:
    print("Error {}".format(e))


class MyDb(object):

    def __init__(self, Table_Name='DHT11'):
        self.Table_Name=Table_Name

        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(Table_Name)

        self.client = boto3.client('dynamodb')

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'sensorID':"1"
            }
        )

        return response

    def put(self, Sensor_Id='', Timestamp='', Temperature='', Humidity=''):
        self.table.put_item(
            Item={
                'sensorID':Sensor_Id,
                'Timestamp':Timestamp,
                'Temperature':Temperature,
                'Humidity' :Humidity
            }
        )

    def delete(self,Sensor_Id=''):
        self.table.delete_item(
            Key={
                'sensorID': Sensor_Id
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='DTH11'
        )
        return response

    @staticmethod
    def sensor_value():

        time = datetime.now()
        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

        gpio = 4
        dht11 = Adafruit_DHT.DHT11

        humidity, temperature = Adafruit_DHT.read_retry(dht11, gpio)

        if humidity is not None and temperature is not None:
            print('Datetime: {0}, Temp: {1:0.1f} C, Humidity: {2:0.1f} %'.format(timestamp, temperature, humidity))
            # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return timestamp, temperature, humidity


def main():
    global counter
    threading.Timer(interval=10, function=main).start()
    obj = MyDb()
    Timestamp, Temperature , Humidity = obj.sensor_value()
    obj.put(Sensor_Id=str(counter), Timestamp = str(Timestamp), Temperature=str(Temperature), Humidity=str(Humidity))
    counter = counter + 1
    print("Uploaded Sample on Cloud Ts: {}, Temp:{}, Hum:{} ".format(Timestamp,Temperature, Humidity))


if __name__ == "__main__":
    global counter
    counter = 0
    main()
