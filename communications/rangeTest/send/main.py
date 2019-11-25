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
    logger.debug("Sending test file")
    f = open("testFile.txt", "r")
    f1 = f.readlines()
    for x in f1:
        logger.debug(x)
        com.send(x)
    f.close()
    #file sent, inform the receiver
    logger.debug("File sent")
    com.send("EndOfFile")
    


    # Program end
    logger.debug("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    COM_CONNECTION_STRING = 'COM3'
    main()
