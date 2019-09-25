import os, sys
from temp_sensors import temp_sensors
from motion_det import motion_det

tempThresh = 40
humThresh = 10

while True:
    Temp,Humidity = temp_sensors.temp_data()
    Motion = motion_det.motion_data()

    C = Temp
    H = Humidity

    if C!=-1000 or H!=-1000:
        if C>tempThresh or H>humThresh or Motion==True:
            os.system('say "Motion Detected"')