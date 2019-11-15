"""
Test program that:
connects to xbee unit on COM4, which is determined by current computer
waits to recieve audio file as a series of bytes
ends if number of bytes received matches expected number of bytes
times out if nothing received for 20 seconds (timeout)
stores information in receivedAudio.wav
stores all actions in a continuing log

"""

import logging
import sys
import time
import wave
import serial
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
    f = wave.open("receivedWavFile.wav", "w")



    #hardcoded file format
    n_channels = 1
    sample_width = 2
    framerate = 44100
    n_frames = 204800
    comp_type = "NONE"
    comp_name = "not compressed"

    params = (n_channels, sample_width, framerate, n_frames, comp_type, comp_name)
    f.setparams(params)

    audioData = b""
    x = com.receiveAudio()
    #iterate over file size
    #100 frames
    bytesSent = 0
    lastBytesSent = 0
    byteNumber = 0
    fileSize = n_frames * sample_width * n_channels
    timeout = 20

    timeFlag = time.time()
    while byteNumber < fileSize:
        #valid data
        if x != b"":
            timeFlag = time.time()
            byteNumber = byteNumber + 1
            #valid data
            #append to data
            audioData = audioData + x
            bytesSent = bytesSent + 1
            if bytesSent >= lastBytesSent + 1024:
                lastBytesSent = lastBytesSent + 1024
                logger.debug(bytesSent)
                
        x = com.receiveAudio()
        if (timeFlag + timeout < time.time()):
            logger.debug("Timeout")
            break

    #transmission finished, write to file
    f.writeframesraw(audioData)
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
