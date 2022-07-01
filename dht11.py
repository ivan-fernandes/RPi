from time import sleep
from datetime import datetime
import Adafruit_DHT
from RPLCD import CharLCD
from RPi import GPIO
import os

# store datetime, temperature and humidity in a csv file.
csvfile_name = 'dht11.csv'
# If it does not exist, create it.
if not os.path.isfile(f"./{csvfile_name}"):
    a = open(f"./{csvfile_name}", "w+")
    a.close()

# set up the LCD
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

# Set up the DHT11 sensor and pin
gpio = 24
dht11 = Adafruit_DHT.DHT11

while True:
    time = datetime.now()
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

    humidity, temperature = Adafruit_DHT.read_retry(dht11, gpio,delay_seconds=2)

    # save to a csv file
    with open(f"{csvfile_name}", 'a') as f:
        f.write("{},{},{}\n".format(timestamp, temperature, humidity))

# Output to an LCD
# https://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/
# Connect (D4,D5, D6, D7) to pins (33, 31, 29, 23), Rs e Rw to pins (37, 35), Ground to pin 39 and VCc to pin 2 (5V)
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Temp: {0:0.1f} C'.format(temperature))
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Humidity: {0:0.1f} %'.format(humidity))

# Output to an SSH terminal
    print('Datetime: {0}, Temp: {1:0.1f} C, Humidity: {2:0.1f} %'.format(timestamp, temperature, humidity))
    sleep(30)
#    lcd.clear() # Clear display
