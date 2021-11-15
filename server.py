##########################################################################
#        Name: server.py
# Description: The server handling all of the clients connecting to chat.
#  Created on: November 10, 2021
#  Updated on: November 14, 2021
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

  def receive_msg(self, connection) -> str:
    """
    Receives the message from the client. 
    It receives the message length first, then it receives the actual message.
    Returns the message. If message not received, then return an empty string.
    """
    msg_length = connection.recv(HEADER_LENGTH).decode(HEADER_FORMAT)
    if msg_length:
      msg_length = int(msg_length)
      msg = connection.recv(msg_length).decode(HEADER_FORMAT)
      return msg
    return ""

  def get_name(self, connection) -> str:
    """
    Handles the process of receiving the name from the client.
    Returns a string for the name received from the client.
    """
    name = ""
    while name == "":
      connection.send("Please enter a name.".encode(HEADER_FORMAT))
      name = self.receive_msg(connection=connection)
    return name

  def handle_connection(self, connection, address) -> None:
    """
    Handles the connection with the client.
    """
    print(f"[CONNECTION] {address} connected")
    connected = True
    name = self.get_name(connection)
    connection.send(f"Hello {name}.".encode(HEADER_FORMAT))
    while connected:
      msg_from_client = self.receive_msg(connection)
      if DISCONNECT_MESSAGE in msg_from_client.upper():
        connected = False
      print(f"[CLIENT {address[1]}] {msg_from_client}")
    print(f"[CONNECTION] {address} disconnected")
    connection.close()

  def start(self) -> None:
    print("[SERVER] starting server...")
    self.server.listen()
    print(f"[SERVER] listening on {IP_ADDRESS}:{PORT}")
    while True:
      connection, address = self.server.accept()
      thread = threading.Thread(target=self.handle_connection, args=(connection, address))
      thread.start()
      print(f"[CONNECTION] current active connections: {threading.active_count() - 1}")

def main():
  try:
    server = Server()
    server.start()
  except KeyboardInterrupt:
    print("\n[SERVER] shutting down server...")

if __name__ == "__main__":
  main()