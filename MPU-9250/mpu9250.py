from time import sleep
from datetime import datetime
import os
from RPLCD import CharLCD
from RPi import GPIO
from mpu9250_i2c import *

# wiring and sample code from https://makersportal.com/blog/2019/11/11/raspberry-pi-python-accelerometer-gyroscope-magnetometer


# # store datetime, temperature and humidity in a csv file.
# csvfile_name = 'mpu9250.csv'
# # If it does not exist, create it.
# if not os.path.isfile(f"./{csvfile_name}"):
#     a = open(f"./{csvfile_name}", "w+")
#     a.close()

# set up the LCD
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])


sleep(1) # delay to allow MPU9250 to settle
print('Recording data...')

while True:
    time = datetime.now()
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    try:
        ax,ay,az,gx,gy,gz = mpu6050_conv() # read and convert mpu9250 data (accelerometer and gyroscope, X Y Z)
        # mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data (X Y Z)
    except:
        continue

    # # save to a csv file
    # with open(f"{csvfile_name}", 'a') as f:
    #     f.write("{},{},{}\n".format(timestamp, temperature, humidity))

# # Output to an LCD
# # Connect (D4,D5, D6, D7) to pins (33, 31, 29, 23), Rs e Rw to pins (37, 35), Ground to pin 39 and VCc to pin 2 (5V)
#     lcd.cursor_pos = (0, 0)
#     lcd.write_string('Accel: {0:0.1f} C'.format(temperature))
#     lcd.cursor_pos = (1, 0)
#     lcd.write_string('Gyro: {0:0.1f} %'.format(humidity))

# Output to an SSH terminal
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
    print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(gx,gy,gz))
    # print('mag [uT]:   x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx,my,mz))
    print('{}'.format('-'*30))
    sleep(3)

# explanation of the readings
# accelerometer ax,ay,az = acceleration in g
# z when the device is leveled should be near 1 (gravity acting vertically and downwards)
# gyroscope: gx,gy,gz = angular velocity in degrees per second
# if we are not moving the device, this value should be near 0
# magnetometer: mx,my,mz = magnetic field strength in microteslas (uT) - shows the mx my of the earths magnetic field where you are located

#    lcd.clear() # Clear display
