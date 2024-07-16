"""
Reaction Wheel Inverted Pendulum
Original created by: Brick Experiment Channel
Modified by: Instabiel
Hardware:
   MPU9250 IMU
   Some Servo
"""

#settings
ANGLE_FILTER_G    = 0.999   #gyro portion of complementary filter [0...1]
ANGLE_LIMIT       = 45      #stop program / start rise up sequence [deg]
MOTORCTRL_CUT_OFF = 0.1     #At what value to "cut off" the motorCtrl. Helps with stutters at low currents.
RISEUP_END_ANGLE  = 5       #stop rise up sequence and start balancing [deg]
ANGLE_FIXRATE     = 1.      #variate target angle [deg/s]
ANGLE_FIXRATE_2   = 0.5     #reduce continuous rotation
KP                = 2    #PID proportional factor
KI                = 0.05    #PID integral factor
KD                = 0.004       #PID derivative factor
MOTOR_R           = 20      #motor resistance [Ohm]
MOTOR_Ke          = 0       #motor back EMF constant [Vs/rad]
SUPPLY_VOLTAGE    = 5       #battery box voltage [V]
SLEEP_TIME        = 1       #main loop sleep [ms]
NAN_WARNINGS      = True    #warnings of NaNs from measurements
PRINTTIME         = 1e-9    #print time interval [s]
MOTOR_MAX         = 100      #min/max value motorCtrl before usage

############################################################

import os
import warnings
from time import sleep, perf_counter_ns
from datetime import datetime
import math
import signal
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
from gpiozero import DigitalInputDevice, DigitalOutputDevice, PWMOutputDevice, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

#prepare IMU sensor
imu = MPU9250(bus=1, gfs=GFS_250, afs=AFS_2G)
imu.abias = [0.013221153846153846, -0.030993339342948716, 0.004657451923076872]
imu.gbias = [1.3726094563802083, 1.2428309122721355, 0.10033772786458334]
imu.configure()



#prepare motor controller
try:
    my_factory = PiGPIOFactory()  #hardware pwm supported
except:
    os.system("sudo pigpiod")
    print("Started Pi GPIO")
    sleep(2)
    my_factory = PiGPIOFactory()  #hardware pwm supported
servo = Servo(17, min_pulse_width=1e-3, max_pulse_width=2e-3, pin_factory=my_factory)
rechtsom = servo.min
linksom = servo.max
stopom = servo.mid
motorctrl = 0

#exit program when Ctrl-C is pressed
exitRequested = False
def sigintHandler(sig, frame):
    print("Ctrl-C pressed, exit program")
    global exitRequested
    exitRequested = True
signal.signal(signal.SIGINT, sigintHandler)
signal.signal(signal.SIGTERM, sigintHandler)

print("program started")

startTime = perf_counter_ns()
prevLoopTime = perf_counter_ns()
prevPrintTime = perf_counter_ns()
loopCount = 1
gyroAngle = float('nan')
measuredAngle = float('nan')
risingUp = False
targetAngle = 0
error = 0
prevError = 0
integral = 0
derivative = 0
PIDoutput = 0
motorCtrl = 0
logData = [["secondsSinceStart","accAngle","gyroAngle","measuredAngle","targetAngle","error","integral","derivative","PIDoutput","motorCtrl"]]

while not exitRequested:
    timeDelta = (perf_counter_ns() - prevLoopTime) / 1e9  #[sec]
    prevLoopTime = perf_counter_ns()
    secondsSinceStart = (perf_counter_ns() - startTime) / 1e9
    
    #read accelerometer
    ax, ay, az = imu.readAccelerometerMaster()  #[G]
    accAngle = -math.atan(-ax / math.sqrt(pow(ay, 2) + pow(az, 2)+1e-9) + 1e-12) * (180 / math.pi)  #[deg]
    
    #read gyroscope
    gx, gy, gz = imu.readGyroscopeMaster()  #[deg/s]
    gyroAngleDelta = gz * timeDelta
    if math.isnan(gyroAngle): 
        gyroAngle = accAngle
        if NAN_WARNINGS: warnings.warn("gyroAngle = NaN!")
    gyroAngle += gyroAngleDelta  #[deg]
    
    #calculate arm angle (complementary filter)
    if math.isnan(measuredAngle): 
        measuredAngle = accAngle
        if NAN_WARNINGS and loopCount>1: warnings.warn("measuredAngle = NaN!")
    measuredAngle = (ANGLE_FILTER_G * (measuredAngle + gyroAngleDelta) + (1-ANGLE_FILTER_G) * accAngle)  #[deg]
        
    
    #safety check
    if abs(measuredAngle) >= ANGLE_LIMIT:
        if secondsSinceStart < 0.001:
            print("START RISE UP SEQUENCE")
            risingUp = True
        elif not risingUp:
            print("PROGRAM STOPPED, angle is too large: %.2f" % (measuredAngle))
            break
    
    #rise up sequence
    if risingUp:
        if secondsSinceStart < 1.0:
            #speed up reaction wheel to full speed
            rechtsom()
        elif secondsSinceStart < 1.5:
            #change direction using full power
            linksom()
            
            #wait until close to top position, then start balancing
            if abs(measuredAngle) < RISEUP_END_ANGLE:
                print("END RISE UP SEQUENCE")
                risingUp = False
        else:
            print("RISE UP TIMEOUT")
            break

    else:
    
        #variate target angle
        if measuredAngle < targetAngle:
            targetAngle += ANGLE_FIXRATE * timeDelta
        else:
            targetAngle -= ANGLE_FIXRATE * timeDelta
        
        #reduce continuous rotation
        targetAngle -= ANGLE_FIXRATE_2 * timeDelta
        
        #PID controller
        error = targetAngle - measuredAngle
        integral += error * timeDelta
        derivative = (error - prevError) / timeDelta
        prevError = error
        PIDoutput = KP * error + KI * integral + KD * derivative
        
        #compensate for motor back EMF voltage
        current = -PIDoutput
        voltage = MOTOR_R * current + MOTOR_Ke
        
        #convert voltage to pwm duty cycle
        motorCtrl = voltage / SUPPLY_VOLTAGE
        
        #drive motor
        motorCtrl = min(max(motorCtrl, -MOTOR_MAX), MOTOR_MAX)
        if abs((1/MOTOR_MAX)*0.5*motorCtrl) <= MOTORCTRL_CUT_OFF:
            servo.value = None
        else:
            servo.value = -(1/MOTOR_MAX)*0.5*motorCtrl
        
    
    #log data for post analysis
    logData.append([secondsSinceStart, accAngle, gyroAngle, measuredAngle, targetAngle, error, integral, derivative, PIDoutput, motorCtrl])
    
    #debug print
    if (perf_counter_ns() - prevPrintTime) * PRINTTIME >= 1.0:
        secondsSinceLastPrint = (perf_counter_ns() - prevPrintTime) * PRINTTIME
        prevPrintTime = perf_counter_ns()
        loopInterval = secondsSinceLastPrint / loopCount * 1e-3
        loopCount = 0
        print("measuredAngle: %.2f, motorCtrl: %.2f, loopInterval: %.2f ms"
              % (measuredAngle, motorCtrl, loopInterval))
    
    sleep(SLEEP_TIME * 1e-3)
    loopCount += 1

#stop motor
servo.value = None

def SelectDirectory(**kwargs) -> str:
    """Returns the directroy to save datalogs, will make a new directory if it did not exist"""
    path = kwargs.pop('path', os.path.dirname(__file__)+"datalogs")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

#write log data to file
print("log size", len(logData), "rows")
if len(logData) > 0:
    #filename = "datalog.dat"
    filename = os.path.join(SelectDirectory(), "datalog_" + datetime.now().strftime("%d_%H:%M") + ".dat")
    print("write to file:", filename)
    file = open(filename, "w")
    for logLine in logData:
        for value in logLine:
            file.write(str(value) + ' ')
        file.write('\n')
    file.close()

print("program ended")