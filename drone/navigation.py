'''
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
'''

from dronekit import connect, LocationGlobal, LocationGlobalRelative, Vehicle, VehicleMode, Command
from pymavlink import mavutil
import time, math, dronekit_sitl


#This block of code connects to the UAV over its serial connection, Pi -> PixHawk
#It also initalizes the vehicle object referenced throughout this file.
#When the connection information is known, fill out the portInformation variable to disable auto-start of SITL.
portInformation = None
testSITL = None

if not portInformation:
    testSITL = dronekit_sitl.start_default()
    portInformation = testSITL.connection_string()
    print("Starting SITL Test Environment, No UAV Detected")

print("Connecting to UAV.")
UAV = connect(portInformation, wait_ready=True)

#wait for radio transmission from ground station UI, store transmitted values into this array
#0-1 are ISU 1 lat/long, 2-3 ISU 2 lat/long, 4-5 gnd station lat/longaa
GPSCoordinates = [[],[],[],[],[],[]];



'''
This function arms the UAV and initializes its takeoff to an altitude determined by the goalAltitude variable.
The only input is the takeoff goal altitude, but returns nothing.
Input Variables: goalAltitude in meters, integer.
'''
def takeoffSequence(goalAltitude):

    print("Takeoff Sequence Initializing. - Ensure area above UAV is clear.")

    while not UAV.is_armable:
        print("UAV Initializing")
        time.sleep(2)

    UAV.mode = VehicleMode("GUIDED")
    UAV.armed = True

    while not UAV.armed:
        print("Arming, please wait.")
        time.sleep(2)

    print("UAV Armed. ")
    print("Initiating takeoff sequence.")
    UAV.simple_takeoff(goalAltitude)


    while not UAV.location.global_relative_frame.alt >= goalAltitude *.90:
        print("Vehicle taking off. Current altitude: ", UAV.location.global_relative_frame.alt)
        time.sleep(1)

    print("Takeoff complete.")

'''
This function takes two LocationGlobalRelative objects and returns the distance between them in meters.
It is based on the ArduPilot file using it at https://github.com/ArduPilot/ardupilot/blob/master/Tools/autotest/common.py
It is also found in the DroneKit documentation at https://dronekit-python.readthedocs.io/en/stable/
Input Variables: Location1, LocationGlobalRelative. Location2, LocationGlobalRelative. 
'''
def distanceRelative(Location1, Location2):

    latitude = Location2.lat - Location2.lat
    longitude = Location2.lon - Location2.lon

    distMeters = math.sqrt((latitude * latitude)+ (longitude * longitude)) * 1.113195e5

    return distMeters

'''
This function is the basic travel-to-point function that will be utilized to travel to each of the ISUs and back
to the ground station in turn.
Input Variables: latitude, float; longitude, float.
'''
def travel(latitude, longitude):

    print("Initializing travel to coordinates: ", latitude, ", ", longitude)
    if not UAV.location.global_relative_frame.alt >= 10:
        print("UAV altitude under 10 meters, aborting travel.")
        return None

    if UAV.system_status == ACTIVE:
        print("UAV active, beginning travel.")

    currentLocation = UAV.location.global_relative_frame
    goalLocation = LocationGlobalRelative(latitude, longitude, 30)

    UAV.simple_goto(goalLocation)
    print("Distance to waypoint: ", distanceRelative(currentLocation, goalLocation), " meter(s)")

    '''while not close'''

    print("Waypoint reached. Commencing hover.")
    return None

#still workin



'''
This function is called when no communication with an ISU can be established. It takes the current location of the
UAV, and plots a search pattern with a number of points based on the input.
Input Variables: searchPoints, integer.
'''
def searchPattern(searchPoints):

    print("Search pattern initializing with ", searchPoints, " discrete points.")

    #First, checking to make sure the UAV is in the air, armed, etc.
    if not UAV.location.global_relative_frame.alt >= 10:
        print("UAV under 10 meters, aborting search pattern.")
        return None

    if UAV.system_status == ACTIVE:
        print("UAV active, beginning search pattern.")


#still workin

