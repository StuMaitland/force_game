import serial

global port


def init():
    global port
    port = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=0.01)


def getforces():
    global port

    bytedata = []
    forces = []
    while port.in_waiting < 12:
        forces = []
    numdata = port.in_waiting
    numdata = int(numdata / 12) * 12
    for i in range(numdata):
        bytedata.append(int.from_bytes(port.read(1), 'little'))
    baforfile = bytearray(bytedata)
    if (bytedata[numdata - 2] == 0x0f) & (bytedata[numdata - 1] == 0xf0):
        for i in range(5):
            forces.append(bytedata[numdata - 12 + i * 2] + 256.0 * bytedata[numdata - 12 + i * 2 + 1])
    else:
        done = 0
        while done == 0:
            if int.from_bytes(port.read(1), 'little') == 0x0f:
                if int.from_bytes(port.read(1), 'little') == 0xf0:
                    done = 1
        for i in range(12):
            bytedata[i] = int.from_bytes(port.read(1), 'little')
        for i in range(5):
            forces.append(bytedata[i * 2] + 256.0 * bytedata[i * 2 + 1])
    for i in range(5):
        forces[i] = -forces[i] + 2048
    return forces


def cleanup():
    global port
    port.close()
