"""
Test program that:
connects to xbee unit on COM4, which is determined by current computer
waits to recieve file
stores information in receivedData.txt
stops on message: "EndOfFile"
stores all actions in a continuing log

"""

import logging
import sys
import time
from communication import Communication



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
    logger.debug("Connected to wireless communication transceiver")


    #Wait to receive file
    logger.debug("Waiting to receive file")
    f = open("receivedData.txt", "w")
    waypoints = com.receive()
    while waypoints != "EndOfFile":
        #valid data
        if waypoints != None:
            #valid data
            logger.debug(waypoints)
            #write to file
            f.write(waypoints)
        waypoints = com.receive()
        #time.sleep(1)
    f.close()



    # Program end
    logger.debug("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    #use for serial port in ISU
    #COM_CONNECTION_STRING = '/dev/ttySO'
    #use for USB port in drone
    #COM_CONNECTION_STRING = '/dev/ttyUSB0'
    #use for USB port in computer, check device manager
    COM_CONNECTION_STRING = 'COM4'
    main()
