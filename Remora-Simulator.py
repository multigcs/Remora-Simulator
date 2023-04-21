import socket
from struct import *

PRU_DATA = 0x64617461
PRU_READ = 0x72656164
PRU_WRITE = 0x77726974
PRU_ACKNOWLEDGE = 0x61636b6e
PRU_ERR = 0x6572726f
PRU_ESTOP = 0x65737470
JOINTS = 6
VARIABLES = 2
INPUTS = 32
OUTPUTS = 32


localIP     = "10.10.10.10"
localPort   = 27181
bufferSize  = 1024

position = [0] * JOINTS

jointEnabled = 0
jointFreq = [0] * JOINTS
jointFeedback = [0] * JOINTS
vinData = [0.0] * VARIABLES
voutData = [0.0] * VARIABLES
inputData = 0
outputData = 0


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))


def send_ack():
    #print("> PRU_ACKNOWLEDGE")
    UDPServerSocket.sendto(pack("<i", PRU_ACKNOWLEDGE), address)

def send_data():
    """
    int32_t header;
    int32_t jointFeedback[JOINTS];
    float 	processVariable[VARIABLES];
    uint32_t inputs;
	uint16_t NVMPGinputs;
    """
    #print("> PRU_DATA")
    params = [PRU_DATA]
    fstr = "<i"
    for num in range(JOINTS):
        fstr += "i"
        params.append(jointFeedback[num])
    for num in range(VARIABLES):
        fstr += "f"
        params.append(vinData[num])
    fstr += "i"
    params.append(inputData)
    fstr += "h"
    params.append(0)
    data = pack(fstr, *params)
    UDPServerSocket.sendto(data, address)



def read_data(data):
    """
	int32_t header;
    int32_t jointFreqCmd[JOINTS];
    float 	setPoint[VARIABLES];
	uint8_t jointEnable;
	uint32_t outputs;
    uint8_t spare0;
    """
    pos = 0
    for num in range(JOINTS):
        jointFreq[num] = unpack('<i', data[pos:pos+4])[0]
        pos += 4
    for num in range(VARIABLES):
        voutData[num] = unpack('<f', data[pos:pos+4])[0]
        pos += 4
    jointEnabled = unpack('<c', data[pos:pos+1])[0]
    pos += 1
    outputData = unpack('<i', data[pos:pos+4])[0]
    pos += 4
    spare = unpack('<c', data[pos:pos+1])[0]
    pos += 1

    for num in range(JOINTS):

        enabled = f"{int(jointEnabled.hex(), 16):08b}"[::-1]
        if enabled[num] == "0":
            continue

        last = jointFeedback[num]
        
        # for PRU_BASEFREQ 120000 (ask my why :))
        jointFeedback[num] += int(jointFreq[num] * ((1<<22) / 1000))
        position[num] += (last - jointFeedback[num])

        if jointFeedback[num] < -2147483648:
            jointFeedback[num] += 4294967295
        elif jointFeedback[num] > 2147483647:
            jointFeedback[num] -= 4294967295

        jointFreq[num] = 0

    print(f"{int(jointEnabled.hex(), 16):08b}  {outputData:016b}  {voutData} {[round(pos/ (1<<22) / 1600, 3) for pos in position]}", end='\r')


print("Enabled   Outputs           Variables")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    header = unpack('<i', message[:4])[0]
    if header == PRU_READ:
        #print("PRU_READ")
        send_data()

    elif header == PRU_WRITE:
        #print("PRU_WRITE")
        read_data(message[4:])
        send_ack()

    else:
        print("Unknown")









