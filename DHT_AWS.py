


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
    def get(self,sensorID=''):
        response = self.table.get_item(
            Key={
                'sensorID':sensorID
            }
        )

        return response

    def put(self, sensorID='Unknown', sample_id='', Timestamp='', Temperature='', Humidity=''):
        self.table.put_item(
            Item={
		'sensorID':sensorID,
                'sample_id':sample_id,
                'Timestamp':Timestamp,
                'Temperature':Temperature,
                'Humidity' :Humidity
            }
        )

    def delete(self,sample_id=''):
        self.table.delete_item(
            Key={
                'sample_id': sample_id
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

        gpio = 24
        dht11 = Adafruit_DHT.DHT11

        humidity, temperature = Adafruit_DHT.read_retry(dht11, gpio)

        if humidity is not None and temperature is not None:
            print('Datetime: {0}, Temp: {1:0.1f} C, Humidity: {2:0.1f} %'.format(timestamp, temperature, humidity))
            # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return timestamp, temperature, humidity


def main():
    global counter, interval, sampling_rate
    obj = MyDb()
    threading.Timer(interval=sampling_rate, function=main).start()
    Timestamp, Temperature , Humidity = obj.sensor_value()
    obj.put(sensorID=sensorID, sample_id=sensorID +'_'+ str(counter), Timestamp = str(Timestamp), Temperature=str(Temperature), Humidity=str(Humidity))
    counter = counter + 1
    print("Uploaded Sample on Cloud Ts: {}, Temp:{}, Hum:{} ".format(Timestamp,Temperature, Humidity))


if __name__ == "__main__":
    global counter
    counter = 0
    global sampling_rate
    sampling_rate = int(input('Define the sampling rate:  '))
    global sensorID
    sensorID = input('Define the sensor ID:  ')
    main()
