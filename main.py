"""Main program for autonomous drone flight and sensor data logging.

Uses the ttyO4 connection (UART4) on the beaglebone to connect to a Pixhawk flight controller.
Uses the ttyO1 connection (UART1) to connect to a xBee wireless communication module.
Uses tcp://localhost:5555 to connect to zmq server for reading i2c sensor data.
Installing the appropriate main.service file allows for this to start on boot.

The waypoints sent from the GCS will be a list of dictionaries in the form:
    {"x" : <int>,       - positive east offset from start location in meters
     "y" : <int>,       - positive north offset from start location in meters
     "z" : <int>}       - altitude in meters

Since the dronekit module was done in Python2 at the time this was written, this program
must conform to Python2 syntax. However, the program running on the GCS is written in Python3
and therefore expects the newer syntax. The most notable side effect from this is that all strings
used by the communication module must be sent as unicode strings.

The sensor data that the GCS expects will be a dictionary in the form:
    {"x" : <int>,       - positive east offset from start location in meters
     "y" : <int>,       - positive north offset from start location in meters
     "z" : <int>,       - altitude in meters
     "temp" : <float>,  - temperature in degrees Celsius
     "lat"  : <float>,  - latitude
     "lon"  : <float>,  - longitude
     "time" : <float>}  - seconds since start of flight path
"""

import logging
import sys
import time
from communication import Communication

# Set max and min allowed distance for the UAV to travel from start location
MAX_RADIUS = 250
MAX_ALTITUDE = 50
MIN_ALTITUDE = 3








def main():
    # Setup logging
    logger = logging.getLogger('control')
    logger.setLevel(logging.DEBUG)
    filehandler = logging.FileHandler('main.log')
    filehandler.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.addHandler(console)

    # Connect to xBee
    com = Communication(COM_CONNECTION_STRING, 0.1)
    logger.debug("Connected to wireless communication receiver")
    com.send(u"Connected to wireless communication receiver")


    # Wait until the waypoints flight path is received from GCS
    logger.debug("Waiting to receive flight path from GCS")
    com.send(u"Waiting to receive flight path from GCS")
    waypoints = com.receive()
    while not waypoints:
        waypoints = com.receive()
        time.sleep(1)

#    # Create points
#    start_location = vehicle_control.vehicle.location.global_relative_frame
#    points = create_waypoints(logger, com, start_location, waypoints)
#
#    if not points:
#        logger.critical("Invalid points received from GCS")
#        com.send(u"Invalid points received from GCS")
#        sys.exit(1)
#
#
#    # Log points
#    for index, point in enumerate(points):
#        logger.debug("Destination {}: {}".format(index, point))


    # Program end
    logger.debug("Finished program.")
    com.send("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    COM_CONNECTION_STRING = '/dev/ttySO'
    main()
