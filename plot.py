from matplotlib import pyplot as plt

fig, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(gpspos_time, knots, 'o-b')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Speed (knots)', color='b')
ax1.tick_params('y', colors='b')
ax12 = ax1.twinx()
ax12.plot(atm_time, baro_alt, 'r')
ax12.set_ylabel('Altitude (m)', color='r')
ax12.tick_params('y', colors='r')

ax2.plot(head_time, heading[:,0])
ax2.set_xlabel('time (s)')
ax2.set_ylabel('Heading')

plt.show()
