import csv
from labjack import ljm
import time

'''
Install the drivers : https://labjack.com/pages/support?doc=/software-driver/installer-downloads/ljm-software-installers-t4-t7-digit/
More info about the library : https://labjack.com/pages/support?doc=/software-driver/ljm-users-guide

'''


def pressure_regulator_control_main():

    # Connection of labkjack
    handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier

        
    # Setup and call eWriteAddress to write a value to the LabJack.
    address_w = 1002  # DAC1
    address_r = 0  # AIN0
    dataType = ljm.constants.FLOAT32
    
    #path of the memory cache
    path_cache=r"mem_cache.txt"
    
    while 1:
        time.sleep(1)
        
        #read cache every seconds
        with open(path_cache) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_=[]
            for row in csv_reader:
                line_.append(row)
        
        #condition to stop the air
        if line_[1][0]=='stop':
            ljm.eWriteAddress(handle, address_w, dataType, 0)
            time.sleep(1)
            break
        
        #sending commands to change the air pressure
        elif line_[1][0] and float(line_[1][0])>=0 and float(line_[1][0])<=5:
            
            pressure_value=float(line_[1][0])
            ljm.eWriteAddress(handle, address_w, dataType, pressure_value)
            pressure_sensor_value = ljm.eReadAddress(handle, address_r, dataType)
            
            print("DAC0 (bar): ", pressure_value)
            print("AIN0 (bar): ", pressure_sensor_value*1.25)
        
        time.sleep(0.5)

    # Close handle
    ljm.close(handle)
