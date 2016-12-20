"""OSC Test Script
Written by Aaron Chamberlain Dec. 2013
The purpose of this script is to make a very simple communication structure to the popular
application touchOSC. This is achieved through the pyOSC library. However, since the pyOSC
documentation is scarce and only one large example is included, I am going to strip down
the basic structures of that file to implement a very simple bi-directional communication.
"""

#!/usr/bin/env python

import socket, OSC, re, time, threading, math

import wave, pyaudio
import SoundModule as sm
import self_state as ss

# receive_address = '172.16.14.197', 7000
# send_address = '172.17.110.168', 8080

receive_address = '192.168.2.2', 7000
send_address = '192.168.2.5', 8080




freq = 4000
pan = 0
cpu = 0

class PiException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Setting up audio

Fs = 22000
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 2,
                        rate = Fs,
                        input = False,
                        output = True)




##########################
#	OSC
##########################

# Initialize the OSC server and the client.
s = OSC.OSCServer(receive_address)
c = OSC.OSCClient()
c.connect(send_address)

s.addDefaultHandlers()

# define a message-handler function for the server to call.
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

def moveStop_handler(add, tags, stuff, source):
	addMove(0,0)

def moveJoystick_handler(add, tags, stuff, source):
	print "message received:"
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "X Value is: "
	print stuff[0]
	print "Y Value is: "
	print stuff[1]  #stuff is a 'list' variable

def martenot_handler(add, tags, stuff, source):
	print "message received:"
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)


	memory_label = "/1/memory"
	msg_label = OSC.OSCMessage()
	msg_label.setAddress(memory_label)
	msg_label.append(cpu)
	# print str(ss.get_cpu(0.001))

	c.send(msg_label)

	global freq, pan
	freq = 400*stuff[0]
	pan = stuff[0]


# adding my functions
s.addMsgHandler("/basic/stop", moveStop_handler)
s.addMsgHandler("/basic/joystick", moveJoystick_handler)
s.addMsgHandler("/mlr/press",moveJoystick_handler)
s.addMsgHandler("/1/fader1",martenot_handler)
# just checking which handlers we have added
# print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr

def periodic_cpu():
	global cpu
	while 1:
		cpu = ss.get_cpu(5)

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever)
cpu_thread = threading.Thread( target = periodic_cpu)
st.start()
cpu_thread.start()


# Loop while threads are running.
try:
	while 1 :
		x = sm.oscTone(0.5,5,freq*700,Fs)
		for k in range(0,len(x)):
			if x[k] > 32767:
				x[k] = 32767
			elif x[k] < -32768:
				x[k] = -32768
		str_out = sm.pan_stereo(x,pan,1-pan)
		stream.write(str_out)
		# cpu = ss.get_cpu(5)

except KeyboardInterrupt:
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()
	print "Done"
