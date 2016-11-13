import socket
import pyaudio
import sys

HOST = 'localhost'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

RATE = 44100

p = pyaudio.PyAudio()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# key = input('Enter key')

# client.listen(5)


while True:

    # data = client.recv(BUFSIZE)
    # print 'server connected ... ', addr
    # myfile = open('testfile.wav', 'w')
    stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )
    client.sendall(sys.argv[1])


    while True:
        data = client.recv(BUFSIZE)
        if not data: break

        stream.write(data)
        # print 'writing file ....'

    stream.close()
    print 'finished writing file'
    client.close()
    print 'client disconnected'
    p.terminate()




