# Client program for the Source module in Marionet.
# Created by Sumanth Srinivasan in December 2016.


import socket

HOST = ''
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

# Create a socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Listen for packets from clients
serv.bind(ADDR)
serv.listen(5)

while True:
  # Accept any connection that is created by a remote client
  conn, addr = serv.accept()
  print 'got client ', addr

  while True:
    # Receive query data
    data = conn.recv(1024)
    if not data: break
    try:
      # This data received is the name of the file, which is then located in the file system
      print data
      file = 'music_dir/' + data + '.wav'

      # Open the file and send it in chunks
      bytes = open(file).read()
      conn.sendall(bytes)
      print 'sending'

    # Error handling for invalid file name
    except IOError as e:
      print e
      print 'Invalid key'
      break

print "sent!"

serv.close()
