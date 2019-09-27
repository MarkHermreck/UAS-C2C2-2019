"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

from dronekit import connect, LocationGlobal, LocationGlobalRelative, Vehicle, VehicleMode, Command
from pymavlink import mavutil
import time, math, dronekit_sitl

'''
This function arms the UAV and initializes its takeoff to an altitude determined by the goalAltitude variable.
The only input is the takeoff goal altitude, and returns the location where the drone took off.
Input Variables: goalAltitude in meters, integer. UAV, UAV object created in main.py
'''
def takeoffSequence(goalAltitude, UAV):
    print("Takeoff Sequence Initializing. - Ensure area above UAV is clear.")

    homeLocation = UAV.location.global_frame

    if not (UAV.battery.level > 90):
        return None
    else:
        print("Vehicle Battery Level: " + str(UAV.battery.level) + "%")

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

    while not UAV.location.global_relative_frame.alt >= goalAltitude * .90:
        print("Vehicle taking off. Current altitude: ", UAV.location.global_relative_frame.alt)
        time.sleep(1)

    print("Takeoff complete.")
    return homeLocation;

'''
This function takes two LocationGlobalRelative objects and returns the distance between them in meters.
It is based on the ArduPilot file using it at https://github.com/ArduPilot/ardupilot/blob/master/Tools/autotest/common.py
It is also found in the DroneKit documentation at https://dronekit-python.readthedocs.io/en/stable/
Input Variables: Location1, LocationGlobalRelative. Location2, LocationGlobalRelative. 
'''
def distanceRelative(Location1, Location2):
    latitude = Location2.lat - Location1.lat
    longitude = Location2.lon - Location1.lon

    distMeters = round(math.sqrt((latitude * latitude) + (longitude * longitude)) * 1.113195e5, 3)


    return distMeters


'''
This function takes a LocationGlobalRelative object and two offset values in meters, and returns another 
LocationGlobalRelative object offset from the original location according to the two values provided.
It is based on the DroneKit documentation at https://dronekit-python.readthedocs.io/en/stable/
Input Variables: ISU, LocationGlobalRelative. offsetNorth, offsetEast, integers in meters.
'''
def searchLocation(ISU, offsetNorth, offsetEast):
    dimensionRad = 6378137.0
    offsetLat = offsetNorth / dimensionRad
    offsetLong = offsetEast / (dimensionRad * math.cos(math.pi * ISU.lat / 180))

    newLat = ISU.lat + (offsetLat * 180 / math.pi)
    newLong = ISU.lon + (offsetLong * 180 / math.pi)

    offsetLocation = LocationGlobalRelative(newLat, newLong, ISU.alt)

    return offsetLocation;


'''
This function is the basic travel-to-point function that will be utilized to travel to each of the ISUs and back
to the ground station in turn.
Input Variables: latitude, longitude, floats. alt, integer. UAV, UAV object created in main.py
'''
def travel(latitude, longitude, alt, UAV):
    print("Initializing travel to coordinates: ", latitude, ", ", longitude)
    if not UAV.location.global_relative_frame.alt >= 10:
        print("UAV altitude under 10 meters, aborting travel.")
        return None

    #if UAV.system_status == ACTIVE:
    #    print("UAV active, beginning travel.")

    currentLocation = UAV.location.global_relative_frame
    goalLocation = LocationGlobalRelative(latitude, longitude, alt)
    totalDistance = distanceRelative(UAV.location.global_relative_frame,goalLocation)

    UAV.simple_goto(goalLocation)
    print("Distance to waypoint: ", distanceRelative(currentLocation, goalLocation), " meter(s)")

    #provides status updates while traveling
    while not (distanceRelative(UAV.location.global_relative_frame, goalLocation)) < 5:
        print("Traveling. Distance remaining: ", distanceRelative(UAV.location.global_relative_frame, goalLocation), " meter(s).")
        time.sleep(2)


    print("Waypoint reached. Commencing hover.")
    return None


'''
This function is called when no communication with an ISU can be established. It takes the current location of the
UAV, and plots a search pattern with an ever-increasingly sized square based on the input. The more points, the larger 
the search square is, with thresholds determining the overall size of the pattern. Minimum points is four.
Each next four increases the diagonal distance from original ISU location by 50 meters.
Input Variables: searchPoints, integer. ISULocation, LocationGlobalRelative. UAV, UAV object created in main.
Returns: 1, indicating successful location of ISU. 0, indicating failure to locate ISU. None, function/input error.
'''
def searchPattern(searchPoints, ISULocation, UAV):
    # 35.355 meters offset to N/E for 50 meter right triangle hypotenuse

    print("Search pattern initializing with ", searchPoints, " discrete points.")

    # First, checking to make sure the UAV is in the air, armed, etc.
    if not UAV.location.global_relative_frame.alt >= 10:
        print("UAV under 10 meters, aborting search pattern.")
        return None

    #if UAV.system_status == ACTIVE:
    #    print("UAV active, beginning search pattern.")

    # Sets searchPoints to the next highest multiple of 4 if it not already set to one.
    if searchPoints % 4 != 0:
        if searchPoints == 0:
            print("Called function with zero search points, aborting.")
            return None;
        searchPoints = searchPoints + (4 - (searchPoints % 4));
        print("Overruling user input, scaling to multiple of 4. Final value: ", searchPoints)

    # generating searchPoints number of locations to ping ISU at
    # these locations are the corners of concentric squares
    # instantiates empty list of size searchPoints

    pingLocs = [None] * searchPoints
    squares = int(searchPoints / 4)

    for x in range(searchPoints):
        corner = x % 4;
        if corner == 0:
            pingLocs[x] = searchLocation(ISULocation, 35.355 * squares, 35.355 * squares)
        if corner == 1:
            pingLocs[x] = searchLocation(ISULocation, -35.355 * squares, 35.355 * squares)
        if corner == 2:
            pingLocs[x] = searchLocation(ISULocation, -35.355 * squares, -35.355 * squares)
        if corner == 3:
            pingLocs[x] = searchLocation(ISULocation, 35.355 * squares, -35.355 * squares)

    # this loop tells the drone to go to each of the locations created above, and ping the ISU
    # exits function upon successful ping, because data can be transferred
    # if it reaches the end of the list with no successful ping, returns 0

    for y in range(searchPoints):

        travel(pingLocs[y].lat, pingLocs[y].lon, ISULocation.alt, UAV)
        # ping drone, return 1 or 0 if success/fail
        placeholder = 3
        if placeholder == 1:
            print("ISU communication established, exiting search pattern successfully.")
            return 1

    print("Search pattern executed, no ISU located. Exiting.")
    return 0


'''
This function handles the landing of the drone, with added safety checks to make sure the drone doesn't
land so enthusiastically it crashes headlong into the ground. It takes the homeLocation of the drone created
in the takeoff
Input Variables: homeLocation, LocationGlobal object created in takeoffSequence(). UAV, UAV object created in main.
'''
def landingSequence(homeLocation, UAV):


    if not distanceRelative(UAV.location.global_relative_frame, homeLocation) < 10:
        print("UAV over 10 meters from ground station, initializing travel.")
        travel(homeLocation.lat, homeLocation.lon, 30, UAV)
        print("Stand by to catch drone.")

    UAV.mode = VehicleMode("RTL")
    UAV.mode = VehicleMode("Land")
    while not UAV.location.global_relative_frame.alt < 2:
        print("Landing. Current altitude: " + UAV.location.global_relative_frame.alt)

    return None

