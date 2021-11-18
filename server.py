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
    self.chatrooms = {}

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

  def handle_connection(self, connection, address) -> None:
    """
    Handles the connection with the client.
    """
    print(f"[CONNECTION] {address} connected")
    connected = True
    name = None
    chatroom_num = None
    connection.send("Please enter a name.".encode(HEADER_FORMAT))
    while connected:
      msg_from_client = self.receive_msg(connection)
      if DISCONNECT_MESSAGE in msg_from_client.upper():
        connected = False
      elif name == None:
        name = msg_from_client
        connection.send(f"Hello {name}.\nPlease enter a chatroom number.".encode(HEADER_FORMAT))
      elif chatroom_num == None:
        try:
          chatroom_num = int(msg_from_client)
          if not (chatroom_num in self.chatrooms):
            self.chatrooms[chatroom_num] = []
          self.chatrooms[chatroom_num].append(connection)
          print(f"[CHATROOM] {address} added to chatroom #{chatroom_num}")
          connection.send(f"--------------------\nWelcome to chatroom #{chatroom_num}!\nEnter {DISCONNECT_MESSAGE} to exit.\n".encode(HEADER_FORMAT))
          for client in self.chatrooms[chatroom_num]:
            if client != connection:
              client.send(f"{name} entered the chat...".encode(HEADER_FORMAT))
        except ValueError:
          connection.send("Please enter a valid chatroom number.".encode(HEADER_FORMAT))
      elif chatroom_num != None:
        for client in self.chatrooms[chatroom_num]:
          if client != connection:
            client.send(f"[{name}] {msg_from_client}".encode(HEADER_FORMAT))

    for client in self.chatrooms[chatroom_num]:
      if client != connection:
        client.send(f"{name} has left the chat...".encode(HEADER_FORMAT))
    print(f"[CONNECTION] {address} disconnected")
    self.chatrooms[chatroom_num].remove(connection)
    connection.close()

  def start(self) -> None:
    print("[SERVER] starting server...")
    self.server.listen()
    print(f"[SERVER] listening on {IP_ADDRESS}:{PORT}")
    while True:
      print(f"[CONNECTION] current active connections: {threading.active_count() - 1}")
      connection, address = self.server.accept()
      thread = threading.Thread(target=self.handle_connection, args=(connection, address))
      thread.start()

def main():
  try:
    server = Server()
    server.start()
  except KeyboardInterrupt:
    print("\n[SERVER] shutting down server...")

if __name__ == "__main__":
  main()