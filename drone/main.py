"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

#importing all the functions and sundries needed from dronekit, mavlink, and the navigation module
from dronekit import connect, LocationGlobal, LocationGlobalRelative, Vehicle, VehicleMode, Command
from pymavlink import mavutil
from navigation import takeoffSequence, distanceRelative, searchLocation, travel, searchPattern, landingSequence, safetyChecks
import time, math, dronekit_sitl

# This block of code connects to the UAV over its serial connection, Pi -> PixHawk
# It also initalizes the vehicle object referenced throughout this file.
# When the connection information is known, fill out the portInformation variable to disable auto-start of SITL.
portInformation = None
testSITL = None

if not portInformation:
    testSITL = dronekit_sitl.start_default()
    portInformation = testSITL.connection_string()
    print("Starting SITL Test Environment, No UAV Detected")

print("Connecting to UAV.")
UAV = connect(portInformation, wait_ready=True)



# wait for radio transmission from ground station UI, store transmitted values into this array
# 0-1 are ISU 1 lat/long, 2-3 ISU 2 lat/long, 4-5 gnd station lat/long
GPSCoordinates = [];

#default location is canberra, australia
#-35.363261
#149.1652299
print(UAV.location.global_relative_frame.lat)
print(UAV.location.global_relative_frame.lon)

homeLoc = takeoffSequence(30, UAV)
#travel(-35.364,149.167,30, UAV)
#searchPattern(3, UAV.location.global_relative_frame, UAV)
landingSequence(homeLoc,UAV)

UAV.close()

if sitl is not None:
    sitl.stop()
