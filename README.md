## simple python-script to simulate Remora-NVEM Ethernet-Protocol 

[![Demo-Video](http://img.youtube.com/vi/TvQcjYgHKG8/0.jpg)](https://www.youtube.com/watch?v=TvQcjYgHKG8 "Demo-Video")


if you run this script on the same host as LinuxCNC, first start LinuxCNC then this script

You need this LinuxCNC Components:

 https://github.com/scottalford75/Remora-NVEM


please update the PRU_BASEFREQ in remora-nv.h:
```
 #define PRU_BASEFREQ		120000
```

or find a working value in the python-script:
```
 jointFeedback[num] += int(jointFreq[num] * ((1<<22) / 1000))
```

