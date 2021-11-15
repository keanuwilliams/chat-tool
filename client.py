##########################################################################
#        Name: client.py
# Description: Connects to the server to attempt to join a chat room to
#              chat with others that join the same chat room.
#  Created on: November 10, 2021
#  Updated on: November 14, 2021
#      Author: Keanu Williams
##########################################################################
# Imports
import socket

##########################################################################
# Macros
HEADER_LENGTH = 128
HEADER_FORMAT = "utf-8"
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_IP_ADDRESS = "192.168.1.29"
PORT = 5050
DISCONNECT_MSG = "!DISCONNECT"

##########################################################################

class Client:
  def __init__(self) -> None:
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start(self) -> None:
    print(f"Connecting to server at {SERVER_IP_ADDRESS}:{PORT}...", end="")
    self.client.connect((SERVER_IP_ADDRESS, PORT))
    print("Connection successful")
    connected = True
    while connected:
      self.receive()
      msg_to_send = ""
      while msg_to_send == "":
        msg_to_send = input(">> ")
      if DISCONNECT_MSG in msg_to_send.upper():
        connected = False
        print("Disconnecting from server...", end="")
      self.send(msg_to_send)
    print("Disconnected successfully")
      
  def receive(self) -> None:
    print(self.client.recv(2048).decode(HEADER_FORMAT))

  def send(self, msg) -> None:
    # Encode the message in the correct format
    msg_to_send = msg.encode(HEADER_FORMAT)
    # Get the length of the message
    msg_length = str(len(msg_to_send)).encode(HEADER_FORMAT)
    # Fill in rest of space
    msg_length += b' ' * (HEADER_LENGTH - len(msg_length)) 
    # Send the message length then send the actual message
    self.client.send(msg_length)
    self.client.send(msg_to_send)

def main():
  try:
    client = Client()
    client.start()
  except ConnectionRefusedError or ConnectionResetError:
    print(f"\n[ERROR] server is not running at {SERVER_IP_ADDRESS}:{PORT}")
  except KeyboardInterrupt:
    client.send(DISCONNECT_MSG)
    print("\nGoodbye.")

if __name__ == "__main__":
  main()