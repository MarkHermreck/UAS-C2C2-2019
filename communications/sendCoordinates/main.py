"""
Test program that:
connects to xbee unit on COM3, which is determined by current computer
sends testFile.txt
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
    logger.debug("Connected to wireless communication tansceiver")


    #Send file
    logger.debug("Sending coordinates")
    x1 = 23.67
    y1 = 0.1823
    x2 = 121.213
    y2 = 123.123
    x3 = 321.321
    y3 = 657.765
    com.send(x1)
    com.send(y1)
    com.send(x2)
    com.send(y2)
    com.send(x3)
    com.send(y3)
    #file sent, inform the receiver
    logger.debug("Coordinates sent")
    com.send("EndOfFile")
    


    # Program end
    logger.debug("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    COM_CONNECTION_STRING = 'COM3'
    main()
