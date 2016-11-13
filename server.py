import socket

HOST = ''
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print serv
serv.bind(ADDR)
serv.listen(5)

while True:
  conn, addr = serv.accept()
  print 'got client bro ', addr

  while True:
    data = conn.recv(1024)
    if not data: break
    try:
      print data
      file = 'music_dir/' + data + '.wav'


      bytes = open(file).read()
      conn.sendall(bytes)
      print 'sending'

    except IOError as e:
      print e
      print 'Invalid key'
      break



print "sent!"

serv.close()
