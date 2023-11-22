
try:
    import os
    import sys
    import datetime
    import time
    import boto3
    import json
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

    def put_db(self, sensorID='Unknown', sample_id='', Timestamp='', Temperature='', Humidity=''):
        self.table.put_item(
            Item={
		'sensorID':sensorID,
                'sample_id':sample_id,
                'Timestamp':Timestamp,
                'Temperature':Temperature,
                'Humidity' :Humidity
            }
        )
        
    # publish mqtt message to AWS IoT
    def publish_mqtt(self, topic='dht/abc', sensorID='Unknown', sample_id='', Timestamp='', Temperature='', Humidity=''):
        client = boto3.client('iot-data')
        response = client.publish(
            topic=topic,
            qos=1,
            payload=json.dumps({
                'sensorID':sensorID,
                'sample_id':sample_id,
                'Timestamp':Timestamp,
                'Temperature':Temperature,
                'Humidity' :Humidity
            })
        )
        return response
    
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

        # if humidity is not None and temperature is not None:
        #     print('Datetime: {0}, Temp: {1:0.1f} C, Humidity: {2:0.1f} %'.format(timestamp, temperature, humidity))
        #     # print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        # else:
        #     print('Failed to get reading. Try again!')
        return timestamp, temperature, humidity


def main():
    global counter, sensorID, sampling_rate
    if not sensorID:
        sensorID='Unknown'
    obj = MyDb()
    threading.Timer(interval=sampling_rate, function=main).start()
    Timestamp, Temperature , Humidity = obj.sensor_value()
    # Put data into DynamoDB
    obj.put_db(sensorID = sensorID,sample_id=sensorID +'_'+ str(counter), Timestamp = str(Timestamp), Temperature=str(Temperature), Humidity=str(Humidity))
    # Publish data to AWS IoT under the specified topic
    obj.publish_mqtt(topic='dht/abc', sensorID=sensorID, sample_id=sensorID +'_'+ str(counter), Timestamp=str(Timestamp), Temperature=str(Temperature), Humidity=str(Humidity))
    # Put data into DynamoDB
    obj.put_db(sensorID=sensorID, sample_id=sensorID +'_'+ str(counter), Timestamp=str(Timestamp), Temperature=str(Temperature), Humidity=str(Humidity))
    counter = counter + 1
    # print("Uploaded Sample on Cloud Ts: {}, Temp:{}, Hum:{} ".format(Timestamp,Temperature, Humidity))


if __name__ == "__main__":
    global counter, sensorID, sampling_rate, topic
    counter = 0
    sampling_rate = int(input('Define the sampling rate:  ') or '600')
    sensorID = input('Define the sensor ID:  ')
    topic = input('Define the topic:  ')
    main()



# MQTT to AWS

# aws iot-data publish --topic "$mqtttopic" --cli-binary-format raw-in-base64-out --payload "{\"id\":'abc1',\"temperature\":$temperature,\"humidity\":$humidity}" --profile "$profile" --region "$region"
# aws iot-data publish --topic "dht/asdfa" --cli-binary-format raw-in-base64-out --payload "{"id":'abc1',"temperature":40,"humidity":80}" --profile ivan --region us-east-1
