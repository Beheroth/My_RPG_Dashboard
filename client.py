import socket


class Client:

   def __init__(self):
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_address = ("localhost", 5555)
      self.id = None

   def connect(self):
      try:
         self.s.connect(self.server_address)
         response = self.s.recv(2048).decode()
         print("{}".format(response))
         self.id = response
      except InterruptedError as e:
         raise e
      except Exception as e:
         pass

   def receive_messages(self):
      data = self.s.recv(2048)


if __name__ == "__main__":
   cli = Client()
   cli.connect()