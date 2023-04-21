simple python-script to simulate Remora-NVEM Ethernet-Protocol 


if you run this script on the same host as LinuxCNC, first start LinuxCNC then this script


You need this LinuxCNC Components:
 https://github.com/scottalford75/Remora-NVEM

please set the PRU_BASEFREQ in remora-nv.h:
 #define PRU_BASEFREQ		120000
 
or find a working value in the python-script:
 jointFeedback[num] += int(jointFreq[num] * ((1<<22) / 1000))



