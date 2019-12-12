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
    x1 = 33.175217
    y1 = -87.605560
    x2 = 33.17541
    y2 = -87.6061
    x3 = 33.175217
    y3 = -87.605560
    com.send(x1)
    com.send(y1)
    com.send(x2)
    com.send(y2)
    com.send(x3)
    com.send(y3)
    #file sent, inform the receiver
    logger.debug("Coordinates sent")
    com.send("EndOfFile")
    

    

    
    n_channels = 1
    sample_width = 2
    framerate = 44100
    n_frames = 204800
    comp_type = "NONE"
    comp_name = "not compressed"

    params = (n_channels, sample_width, framerate, n_frames, comp_type, comp_name)
    

    #Wait to receive 1st text file
    logger.debug("Waiting to receive file")
    f = open("firstTextFile.txt", "w")
    waypoints = com.receive()
    while waypoints != "EndOfFile":
        #valid data
        if waypoints != None:
            #valid data
            logger.debug(waypoints)
            #write to file
            f.write(waypoints)
        waypoints = com.receive()
    f.close()
    




    f = wave.open("firstAudioFile.wav", "w")
    f.setparams(params)
    
    #Wait to receive 1st audio file
    logger.debug("Waiting to receive file")
    audioData = b""
    y = 0
    z = 0
    x = com.read()
    #iterate over file size
    #100 frames
    bytesSent = 0
    lastBytesSent = 0
    byteNumber = 0
    fileSize = n_frames * sample_width * n_channels

    timeFlag = time.time()
    while byteNumber < fileSize:
        #valid data
        if x != b"":
            timeFlag = time.time()
            byteNumber = byteNumber + 1
            #valid data
            bytesSent = bytesSent + 1
            if bytesSent >= lastBytesSent + 1024:
                lastBytesSent = lastBytesSent + 1024
                logger.debug(bytesSent)
        x = com.read()
        if (timeFlag + 5 < time.time()):
            logger.debug("Timeout")
            break
    f.writeframesraw(audioData)
    f.close()



#Wait to receive 1st text file
    logger.debug("Waiting to receive file")
    f = open("secondTextFile.txt", "w")
    waypoints = com.receive()
    while waypoints != "EndOfFile":
        #valid data
        if waypoints != None:
            #valid data
            logger.debug(waypoints)
            #write to file
            f.write(waypoints)
        waypoints = com.receive()
    f.close()
    




    f = wave.open("secondAudioFile.wav", "w")
    f.setparams(params)
    
    #Wait to receive 1st audio file
    logger.debug("Waiting to receive file")
    audioData = b""
    y = 0
    z = 0
    x = com.read()
    #iterate over file size
    #100 frames
    bytesSent = 0
    lastBytesSent = 0
    byteNumber = 0
    fileSize = n_frames * sample_width * n_channels

    timeFlag = time.time()
    while byteNumber < fileSize:
        #valid data
        if x != b"":
            timeFlag = time.time()
            byteNumber = byteNumber + 1
            #valid data
            bytesSent = bytesSent + 1
            if bytesSent >= lastBytesSent + 1024:
                lastBytesSent = lastBytesSent + 1024
                logger.debug(bytesSent)
        x = com.read()
        if (timeFlag + 5 < time.time()):
            logger.debug("Timeout")
            break
    f.writeframesraw(audioData)
    f.close()

    # Program end
    logger.debug("Finished program.")
    sys.exit(0)


if __name__ == "__main__":
    COM_CONNECTION_STRING = 'COM3'
    main()
