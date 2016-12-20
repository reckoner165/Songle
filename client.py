import socket
import pyaudio
import sys
import struct

import OSC, re, time, threading, math



# GLOBAL VARIABLES FOR OSC TO CONTROL EFFECTS
global gain
gain = 0.5

# Socket for client streaming
HOST = 'localhost'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# OSC Setup
osc_ra = '192.168.2.8', 7000 # Receiving Address (This computer)
osc_sa = '192.168.2.5', 8080 # Sending Address (Phone with TouchOSC)

osc_s = OSC.OSCServer(osc_ra)
osc_c = OSC.OSCClient()
osc_c.connect(osc_sa)
#
osc_s.addDefaultHandlers()
#
# # DEFAULT HANDLER. Needs to be expanded with effects
#
def test_handler(addr, tags, stuff, source):
	print "---"
	print "received new osc msg from %s" % OSC.getUrlStr(source)
	print "with addr : %s" % addr
	print "typetags %s" % tags
	print "data %s" % stuff
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "return message %s" % msg
	print "---"

def moveJoystick_handler(add, tags, stuff, source):
    global gain
    print "message received:"
    msg = OSC.OSCMessage()
    msg.setAddress(addr)
    msg.append(stuff)
    osc_c.send(msg)
    # print "X Value is: "
    # print stuff[0]
    gain = stuff[0]
    # print "Y Value is: "
    # print stuff[1]  #stuff is a 'list' variable

osc_s.addMsgHandler("/1/fader1",moveJoystick_handler)

for addr in osc_s.getOSCAddressSpace():
	print addr

print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = osc_s.serve_forever)
st.start()
#

# PyAudio
RATE = 44100
p = pyaudio.PyAudio()

# EFFECTS MODULES WILL BE RIGGED INTO A CHAIN HERE.


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
    # REQUEST FOR MUSIC VIA SYSARG
    client.sendall(sys.argv[1])


    while True:
        global gain
        print gain
        data = client.recv(BUFSIZE)
        if not data: break

        input_tuple = struct.unpack('h'*2048, data)
        effects_in = input_tuple
        # print type(effects_in)
        effects_out = tuple([z * gain for z in effects_in])
        # effects_out = effects_in

        output = struct.pack('h'*2048, *effects_out)

        stream.write(output)
        # print 'writing file ....'

    stream.close()
    print 'finished writing file'
    client.close()
    print 'client disconnected'
    p.terminate()




