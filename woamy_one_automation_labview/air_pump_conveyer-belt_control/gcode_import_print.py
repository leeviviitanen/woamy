import re
from pygcode import Line
from printrun.printcore import printcore
import time
import serial,serial.tools.list_ports
import sys
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

#gcode_path=r"C:\Users\CSMadmin\Desktop\pump_2.0\Square_foamwood100.gcode"

from tkinter import Tk
from tkinter.filedialog import askopenfilename
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
gcode_path = askopenfilename()


def print_main():

    
    findCOM=list(serial.tools.list_ports.grep('1A86:7523')) #find COM of Anet
    p=printcore(findCOM[0][0],115200) # Connect to the printer
    while not p.online: time.sleep(0.1)

    gc=[]
    i=0
    speed_plate=0
    with open(gcode_path, 'r') as fh:
        for line_text in fh.readlines():
            line = str(Line(line_text))

            if len(line.split('G01 X'))>1 :
                gc.insert(i,line.split('E')[0])
                i+=1

    p.send_now("G21") #set units to millimeters
    time.sleep(0.1)
    p.send_now("G90") #use absolute coordinates
    time.sleep(0.1)


    for k in range (2,len(gc)-1):
        # X_Y=re.findall("\d+\.\d+", gc[k])
        # if len(X_Y)>1:
        #     gc[k]=gc[k].replace(X_Y[0],str(float(X_Y[0])*2.67))
        #     gc[k]=gc[k].replace(X_Y[1],str(float(X_Y[1])*2.67))
        
        
        if len(gc[k].split('F'))>1 :
            speed_plate=int(gc[k].split('F')[1])
            
            if speed_plate>2500 :
                speed_plate=0
            
            f = open("speed_cache.txt","r+")
            f.seek(0)
            f.truncate()
            f.writelines(str(speed_plate))
            f.close()

        p.send_now(gc[k])
        print('ok')
        time.sleep(0.3)


    p.send_now("M18")
    p.disconnect()
    f = open("speed_cache.txt","r+")
    f.seek(0)
    f.truncate()
    f.close()


print_main()