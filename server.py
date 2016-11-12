import socket

HOST = ''
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

videofile = 'BeatlesHelpStereo.wav'
bytes = open(videofile).read()
print len(bytes)

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
    print data
    conn.sendall(bytes)


print "sent!"

serv.close()
