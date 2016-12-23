import socket
import pyaudio
import sys
import struct

import OSC, re, time, threading, math

import effects
import SoundModule as sm



# GLOBAL VARIABLES FOR OSC TO CONTROL EFFECTS
# Default values
gain = 0.5
gain_robot = 0.0
pan = 0.5

# Socket for client streaming
HOST = 'localhost'
# HOST = '172.16.31.159'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# OSC Setup
osc_ra = '172.16.11.83', 7000 # Receiving Address (This computer)
osc_sa = '172.17.105.77', 8080 # Sending Address (Phone with TouchOSC)

osc_s = OSC.OSCServer(osc_ra)
osc_c = OSC.OSCClient()
osc_c.connect(osc_sa)
#
osc_s.addDefaultHandlers()
#
# # DEFAULT HANDLER.
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


# Handler to change Main Input gain. It responds to /1/fader1 in TouchOSC
# It also returns the current gain value back to /1/memory
def gain_handler(add, tags, stuff, source):
    global gain
    print "message received:"
    msg = OSC.OSCMessage()
    msg.setAddress("/1/fader1")
    msg.append(stuff)
    osc_c.send(msg)

    gain = stuff[0]

    label_msg = OSC.OSCMessage()
    label_msg.setAddress("/1/memory")
    label_msg.append(gain)
    osc_c.send(label_msg)

# Handler to change Robotization gain. It responds to /1/fader2 in TouchOSC
# It also returns the current robotization gain value back to /1/memory2
def robot_handler(add, tags, stuff, source):
    global gain_robot
    print "message received:"
    msg = OSC.OSCMessage()
    msg.setAddress("/1/fader2")
    msg.append(stuff)
    osc_c.send(msg)

    gain_robot = stuff[0]

    label_msg = OSC.OSCMessage()
    label_msg.setAddress("/1/memory2")
    label_msg.append(gain_robot)
    osc_c.send(label_msg)

def pan_handler(add, tags, stuff, source):
    global pan
    print "message received:"
    msg = OSC.OSCMessage()
    msg.setAddress("/1/fader3")
    msg.append(stuff)
    osc_c.send(msg)

    pan = stuff[0]

    # label_msg = OSC.OSCMessage()
    # label_msg.setAddress("/1/memory2")
    # label_msg.append(gain_robot)
    # osc_c.send(label_msg)

# Patching OSC messages to respective handler functions
osc_s.addMsgHandler("/1/fader1",gain_handler)
osc_s.addMsgHandler("/1/fader2",robot_handler)
osc_s.addMsgHandler("/1/fader3",pan_handler)

for addr in osc_s.getOSCAddressSpace():
	print addr

# Starts a thread to look for OSC packets
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = osc_s.serve_forever)
st.start()
#

# PyAudio
RATE = 44100
p = pyaudio.PyAudio()

while True:
    # data = client.recv(BUFSIZE)
    # print 'server connected ... ', addr
    # myfile = open('testfile.wav', 'w')

    # Setup stream
    stream = p.open(format      = pyaudio.paInt16,
                channels    = 2,
                rate        = RATE,
                input       = False,
                output      = True )
    # REQUEST FOR MUSIC VIA SYSARG
    client.sendall(sys.argv[1])


    while True:
        # Global variables for patching
        global gain, gain_robot,pan
        print gain, gain_robot,pan
        data = client.recv(BUFSIZE)
        if not data:
            print 'no data'
            break

        print 'receiving'
        input_tuple = struct.unpack('h'*2048, data)
        effects_in = input_tuple

        # EFFECTS GO IN
        eff1 = effects.robotization(effects_in, len(input_tuple))

        robot = tuple([z * gain_robot for z in eff1])

        effects_main = tuple([z * gain for z in effects_in])

        effects_out = sm.mix(robot, effects_main)

        effects_out = sm.clip(0.5,1,effects_out)

        # OUTPUT TRACK WITH EFFECTS

        # output = struct.pack('h'*2048, *effects_out)
        output = sm.pan_stereo(effects_out,1-pan,pan)
        stream.write(output)
        print 'writing file ....'

    # Graceful termination
    stream.close()
    print 'finished writing file'
    client.close()
    print 'client disconnected'
    p.terminate()




