##########################################################################
#        Name: server.py
# Description: 
#  Created on: November 10, 2021
#  Updated on: November 10, 2021
#      Author: Keanu Williams
##########################################################################

import socket
import threading

PORT = 5050
IP_ADDRESS = socket.gethostbyname(socket.gethostname())

class Server:
  def __init__(self) -> None:
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server.bind((IP_ADDRESS, PORT))
  
  def handle_client(self):
    pass

  def start(self) -> None:
    pass

def main():
  pass

if __name__ == "__main__":
  main()