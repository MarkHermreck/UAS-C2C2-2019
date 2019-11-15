"""
Test program that:
connects to xbee unit on COM3, which is determined by current computer
sends test1.wav
stores all actions in a continuing log

"""


import logging
import sys
import time
import serial
import wave
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

    #hardcoded file format
    n_channels = 1
    sample_width = 2
    framerate = 44100
    n_frames = 204800
    comp_type = "NONE"
    comp_name = "not compressed"
    

    #Send file
    logger.debug("Sending test file")
    f = wave.open("test1.wav", "rb")
    
    logger.debug("File opened")

    
    bytesSent = 0
    lastBytesSent = 0
    f1 = f.readframes(n_frames)
    
    #send file
    for x in f1:
        com.sendAudio(bytes([x]))
        bytesSent = bytesSent + 1
        if bytesSent >= lastBytesSent + 1024:
            lastBytesSent = lastBytesSent + 1024
            logger.debug(bytesSent)
        
    #file sent
    f.close()
    logger.debug("File sent")

    


    # Program end
    logger.debug("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    COM_CONNECTION_STRING = 'COM3'
    main()
