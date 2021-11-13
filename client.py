##########################################################################
#        Name: client.py
# Description: Connects to the server to attempt to join a chat room to
#              chat with others that join the same chat room.
#  Created on: November 10, 2021
#  Updated on: November 12, 2021
#      Author: Keanu Williams
##########################################################################
# Imports
import socket

##########################################################################
# Macros
HEADER_LENGTH = 128
HEADER_FORMAT = "utf-8"
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_IP_ADDRESS = "192.168.1.144"
PORT = 5050
DISCONNECT_MSG = "!DISCONNECT"

##########################################################################

class Client:
  def __init__(self) -> None:
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((SERVER_IP_ADDRESS, PORT))

def main():
  pass

if __name__ == "__main__":
  main()