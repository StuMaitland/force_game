import serial
import numpy as np

global srrport
global datalen

datalen = 1600  # this needs to match the data length coded in to the microcontroller


# it is 100ms before, 700ms after (200 points, 1400 points at 2kHz)

# initialisation
def init():
    global srrport
    srrport = serial.Serial("/dev/ttyUSB0", baudrate=250000, timeout=1)


# initiate startreact trial, and get EMG response
# trialtype = 0     LED only (VRT)
# trialtype = 1     LED + quiet sound  (VART)
# trialtype = 2     LED +loud sound  (VSRT)
# EMG is returned in integer units, suitable for writing to binary file
# two channels of EMG are in a numpy array, (2,datalen)
# EMG sampling rate is 2kHz
# emg=emg/2048*2.5*10 #converts to mV
def dostartreact(trialtype):
    global srrport
    global emg
    if trialtype == 0:
        srrport.write(b'A\n')
    if trialtype == 1:
        srrport.write(b'B\n')
    if trialtype == 2:
        srrport.write(b'C\n')
    data = srrport.read(datalen * 4)
    data = bytearray(data)
    emg = np.frombuffer(data, dtype='i2')
    emg = emg.reshape(2, datalen)
    return emg


# get button status
# returned as a single byte, where
# bit n is button n, where n is from 0 to 4
def button():
    srrport.write(b'I\n');
    return srrport.read(1)


# control LED targets
# targno negative turns all targets off
# targno=0 turns centre target on immediately
# targno=1..4 turns centre off, and after 200ms gap turns target 1-4 on
def target(targno):
    if targno >= 0:
        s = str(targno)
        srrport.write(bytes(s, 'utf-8'))
        srrport.write(b'\n')
    else:
        srrport.write(b'D\n')  # dark - all LEDs off


# cleanup before quit
def cleanup():
    global srrport
    srrport.close()
