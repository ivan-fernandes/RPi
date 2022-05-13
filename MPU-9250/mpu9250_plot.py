# import libraries
from mpu9250_i2c import *
import smbus,time,datetime
import numpy as np
import matplotlib.pyplot as plt


# prepare for visualization
plt.style.use('ggplot') # matplotlib visual style setting

time.sleep(1) # wait for mpu9250 sensor to settle

ii = 1000 # number of points
t1 = time.time() # for calculating sample rate

mpu6050_str = ['accel-x','accel-y','accel-z','gyro-x','gyro-y','gyro-z']
# AK8963_str = ['mag-x','mag-y','mag-z']
# mpu6050_vec,AK8963_vec,t_vec = [],[],[] # uncomment if magnetometer is used
mpu6050_vec,time_vec = [],[] # comment if magnetometer is used

print('recording data')
for ii in range(0,ii):

    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        # mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
    except:
        continue
    time_vec.append(time.time()) # capture timestamp
    # AK8963_vec.append([mx,my,mz])
    mpu6050_vec.append([ax,ay,az,wx,wy,wz])

print('sample rate accel: {} Hz'.format(ii/(time.time()-t1))) # print the sample rate
time_vec = np.subtract(time_vec,time_vec[0])


# plot the resulting data in 3-subplots, with each data axis
fig,axs = plt.subplots(2,1,figsize=(12,7),sharex=True) # set subplot to 3 if magnetometer is configured
cmap = plt.cm.Set1

ax = axs[0] # plot accelerometer data
for zz in range(0,np.shape(mpu6050_vec)[1]-3):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax.plot(time_vec,data_vec,label=mpu6050_str[zz],color=cmap(zz))
ax.legend(bbox_to_anchor=(1.12,0.9))
ax.set_ylabel('Acceleration [g]',fontsize=12)

ax2 = axs[1] # plot gyroscope data
for zz in range(3,np.shape(mpu6050_vec)[1]):
    data_vec = [ii[zz] for ii in mpu6050_vec]
    ax2.plot(time_vec,data_vec,label=mpu6050_str[zz],color=cmap(zz))
ax2.legend(bbox_to_anchor=(1.12,0.9))
ax2.set_ylabel('Angular Vel. [dps]',fontsize=12)

# ax3 = axs[2] # plot magnetometer data
# for zz in range(0,np.shape(AK8963_vec)[1]):
#     data_vec = [ii[zz] for ii in AK8963_vec]
#     ax3.plot(time_vec,data_vec,label=AK8963_str[zz],color=cmap(zz+6))
# ax3.legend(bbox_to_anchor=(1.12,0.9))
# ax3.set_ylabel('Magn. Field [Î¼T]',fontsize=12)
# ax3.set_xlabel('Time [s]',fontsize=14)

fig.align_ylabels(axs)
plt.show()
