import socket
import threading

server = "localhost"
port  = 5555


def threaded_client(connection: socket.socket):
   print("threaded {}".format(connection))
   connection.send(str.encode("Connected!"))
   while True:
      try:
         data = connection.recv(2048)
         if not data:
            break
         reply = data.decode("utf-8")
         print("{}".format(reply))
         connection.sendall(str.encode(reply))
      except KeyboardInterrupt:
         raise
      except Exception as e:
         print("{}".format(e))
   print("closing {}".format(connection))


def init():
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
      s.bind((server, port))
   except socket.error as e:
      print(str(e))

   s.listen(4)
   print("Waiting for connection on {}".format(s))

   while True:
      connection, address = s.accept()
      print("connected to {}".format(address))

      t = threading.Thread(target=threaded_client, args=(connection,))
      t.start()


if __name__ == "__main__":
   init()
