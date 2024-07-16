import RPi.GPIO as GPIO
import time
import numpy as np
from time import sleep, perf_counter_ns
import math
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import numpy as np
import matplotlib.pyplot as plt
import threading

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11, GPIO.OUT)
servo1 = GPIO.PWM(11, 100)  # pin 11 for servo1, pulse 50Hz

# Start PWM running, with a value of 0 (pulse off)
servo1.start(0)

# Define lists for angles
f_Angle = []
g_Angle = []
a_Angle = []

# Global variable to indicate whether data reading is complete
data_reading_complete = False

# Function to control servo motion
def servo_control():
    duty1 = 13
    duty2 = 28
    while not data_reading_complete:
        print(f"Duty level is {duty1}")
        servo1.ChangeDutyCycle(duty1)
        time.sleep(2)
        print(f"Duty level is {duty2}")
        servo1.ChangeDutyCycle(duty2)
        time.sleep(2)

# Function to read sensor data
def read_sensor_data():
    global data_reading_complete
    imu = MPU9250(bus=1, gfs=GFS_250, afs=AFS_2G)
    imu.abias = [0.013221153846153846, -0.030993339342948716, 0.004657451923076872]
    imu.gbias = [1.3726094563802083, 1.2428309122721355, 0.10033772786458334]
    imu.configure()

    startTime = perf_counter_ns()
    lastGyroTime = perf_counter_ns()
    lastPrintTime = perf_counter_ns()
    time = 0
    loopCount = 0
    gyroAngle = float('nan')
    filteredAngle = float('nan')

    while time < 10:
        # read accelerometer
        ax, ay, az = imu.readAccelerometerMaster()  # [G]
        accAngle = math.atan(-ax / math.sqrt(pow(ay, 2) + pow(az, 2))) * 180 / math.pi  # [deg]

        # read gyroscope
        gx, gy, gz = imu.readGyroscopeMaster()  # [deg/s]
        timeDelta = (perf_counter_ns() - lastGyroTime) / 1e9  # [sec]
        lastGyroTime = perf_counter_ns()
        gyroAngleDelta = gz * timeDelta
        if math.isnan(gyroAngle): gyroAngle = accAngle
        gyroAngle += gyroAngleDelta  # [deg]

        # complementary filter
        if math.isnan(filteredAngle): filteredAngle = accAngle
        filteredAngle = 0.999 * (filteredAngle + gyroAngleDelta) + 0.001 * accAngle

        # debug print
        if (perf_counter_ns() - lastPrintTime) / 1e9 >= 1.0:
            secondsSincePrint = (perf_counter_ns() - lastPrintTime) / 1e9
            lastPrintTime = perf_counter_ns()
            loopInterval = secondsSincePrint / loopCount * 1000
            loopCount = 0
            print("accAngle %.2f, gyroAngle %.2f, filteredAngle %.2f, loopInterval %.2f ms"
                  % (accAngle, gyroAngle, filteredAngle, loopInterval))

        sleep(0.001)
        loopCount += 1
        time += 0.0025

        # Append angles to lists
        a_Angle.append(accAngle)
        f_Angle.append(filteredAngle)
        g_Angle.append(gyroAngle)

    data_reading_complete = True  # Set the flag to indicate data reading is complete

# Create threads for servo control and sensor data reading
servo_thread = threading.Thread(target=servo_control)
sensor_thread = threading.Thread(target=read_sensor_data)

# Start both threads
servo_thread.start()
sensor_thread.start()

# Wait for both threads to finish
servo_thread.join()
sensor_thread.join()

# Cleanup GPIO
servo1.stop()
GPIO.cleanup()

# Save data to CSV file
data = np.array([a_Angle, g_Angle, g_Angle])
file_path = 'sensor_test2.csv'
np.savetxt(file_path, data, delimiter=',')
print(f"CSV file '{file_path}' has been created.")

# Plot the angles
plt.plot(a_Angle, label='$Angle_{acc}$')
plt.plot(g_Angle, label='$Angle_{gyro}$')
plt.plot(f_Angle, label='$Angle_{filtered}$')
plt.xlabel('Time [s]')
plt.ylabel('Degrees [°]')
plt.grid()
plt.legend()
plt.show()