import socket
import numpy as np
import cv2 as cv

UDP_IP = "127.0.0.1"
UDP_PORT = 8021
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
bufferSize = 60000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
for x in range(1000):
    msg = "/SETPARAMS?WIDTH=640&QUALITY=50" + str(x)  # Param queue
    MESSAGE = msg.encode()
    print("message: %s" % MESSAGE)

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    udpReceivedData = sock.recvfrom(bufferSize)

    datagramFromClient = udpReceivedData[0]

    datagramSourceAddress = udpReceivedData[1]

    print(udpReceivedData)

    readFlag = cv.IMREAD_COLOR
    # resp = urlopen(self.urlOperation)
    # image = np.asarray(bytearray(resp.read()), dtype="uint8")

    image = np.asarray(bytearray(datagramFromClient), dtype="uint8")
    image = cv.imdecode(image, readFlag)

    cv.imshow('image', image)
    cv.waitKey(100)
