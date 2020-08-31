import sys
txt = ''
with open(("/home/zy/Rpi3BAndSamb/src/download/aria2/aria2.conf"),'r+') as f:
    txts = f.readlines()
    for s in txts:
        txt += s

pass