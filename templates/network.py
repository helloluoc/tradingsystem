from socket import *
import struct

sendData = struct.pack("!H8sb5sb",1,b"test.jpg",0,b"octet",0)
udpSocket = socket(AF_INET, SOCK_DGRAM)
udpSocket.sendto(sendData, ("192.168.1.226", 69))