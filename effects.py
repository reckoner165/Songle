'''
This file contains modules for different effects and tools to modilfy or filter 
input stream of audio. This file is a part of DSP final project. 
'''
# 
# Created by 
# Drumil Mahajan, New York University, School of Engineering, 
# Class of 2017. 

import random
import cmath
import pyaudio
import struct
import wave
import math
import numpy as np
	
	
def clip_n(input_data, n):
	'''
	This function takes two arguments.
	stream is a floating point number
	n is an integer

	This funtions bound the value of input_data between max and min of n bit signed number
	'''
	
	MAX = 2**(n-1) - 1
	MIN = -2**(n)
	if input_data > MAX:  
		return MAX
	elif input_data < MIN:
		return MIN
	else:
		return input_data


def robotization(input_tuple, BLOCKSIZE): 
	'''
	Parameters : 
	BLOCKSIZE : size of the block, type int
	input_string : input tuple of audio data of size BLOCKSIZE, type int
	
	Returns: 
	output_block : list of output data. type int 
	
	Brief: 
	Converts the input_string into robotized output_block
	'''
	

	output_block = [0 for n in range(0, BLOCKSIZE)]

	spect = np.fft.fft(input_tuple)
	output = np.fft.ifft(np.absolute(spect))
	for n in range(0,len(output)):
		output_block[n] = clip_n(output[n], 16)
	# output_block[n] = output[n]
	#output_string = struct.pack('h' * 2 *  BLOCKSIZE, *output_block)
	return output_block

def whisperisation(input_tuple, BLOCKSIZE):
	'''
	Parameters :
	BLOCKSIZE : size of the block, type int
	input_string : input tuple of audio data of size BLOCKSIZE, type int

	Returns:
	output_block : list of output data. type int

	Brief:
	Converts the input_string into whisperization output_block
	'''

	output_block = [0 for n in range(0, BLOCKSIZE)]

	random_phase = 2 * cmath.pi * random.random()
	random_complex = cmath.cos(random_phase) + (cmath.sin(random_phase))*1j

	spect = np.fft.fft(input_tuple)
	output = np.fft.ifft(np.absolute(spect) * random_complex)

	for n in range(0,len(output)):
		output_block[n] = clip_n(output[n], 16)

	return output_block
	

def vibrato(BLOCKSIZE , f0 , W):

	# Create a buffer (delay line) for past values
	buffer_MAX =  1024                          # Buffer length
	buffer = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

	# Buffer (delay line) indices
	kr = 0  # read index
	kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
	kw = buffer_MAX/2

	# Get previous and next buffer values (since kr is fractional)
    kr_prev = int(math.floor(kr))
    kr_next = kr_prev + 1
    frac = kr - kr_prev    # 0 <= frac < 1
    if kr_next >= buffer_MAX:
        kr_next = kr_next - buffer_MAX

    # Compute output value using interpolation
    output_value = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]

    # Update buffer (pure delay)
    buffer[kw] = input_value

    # Increment read index
    kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        # Note: kr is fractional (not integer!)

    # Ensure that 0 <= kr < buffer_MAX
    if kr >= buffer_MAX:
        # End of buffer. Circle back to front.
        kr = 0

    # Increment write index
    kw = kw + 1
    if kw == buffer_MAX:
        # End of buffer. Circle back to front.
        kw = 0


def butter_bandpass(data, lowcut, highcut, fs, order):
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	y = lfilter(b, a, data)
	return y

	
	
