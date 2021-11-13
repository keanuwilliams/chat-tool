##########################################################################
#        Name: server.py
# Description: The server handling all of the clients connecting to chat.
#  Created on: November 10, 2021
#  Updated on: November 12, 2021
#      Author: Keanu Williams
##########################################################################
# Imports
import socket
import threading

##########################################################################
# Macros
HEADER_LENGTH = 128
HEADER_FORMAT = "utf-8"
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"

##########################################################################

class Server:
  def __init__(self) -> None:
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((IP_ADDRESS, PORT))

  def handle_connection(self, connection, address):
    connection.close()

  def start(self) -> None:
    self.server.listen()
    while True:
      connection, address = self.server.accept()
      thread = threading.Thread(target=self.handle_connection, args=(connection, address))
      thread.start()

def main():
  server = Server()
  server.start()

if __name__ == "__main__":
  main()