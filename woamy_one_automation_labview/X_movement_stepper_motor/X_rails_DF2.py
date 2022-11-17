from printrun.printcore import printcore
import time
import serial,serial.tools.list_ports
import threading
from playsound import playsound
import random


def X_actuator_normal(X,F,iteration):
    s0 = open(r"C:\Users\CSMadmin\Desktop\pump_2.0\stop_cache.txt","r+")
    s0.seek(0)
    s0.truncate()
    s0.close()

    findCOM=list(serial.tools.list_ports.grep('1A86:7523')) #find COM of Anet
    global p
    p=printcore(findCOM[0][0],115200) # Connect to the printer  
    while not p.online: time.sleep(0.1)
    
    p.send_now("G91") 
    time.sleep(0.5)
    for k in range (0,int(iteration)):
        p.send_now("G1 X" + str(X*2.67) + " F" + str(F))
        time.sleep(abs(166.1345*X/F)-3.3)
        playsound(r"C:\Users\CSMadmin\Desktop\pump_2.0\notification.mp3")
        if not p.online: break
        
        p.send_now("G1 X" + str(-X*2.67) + " F" + str(F))
        time.sleep(abs(166.1345*X/F)-3.3)
        playsound(r"C:\Users\CSMadmin\Desktop\pump_2.0\notification.mp3")
        if not p.online: break



    s0 = open(r"C:\Users\CSMadmin\Desktop\pump_2.0\stop_cache.txt","r+")
    s0.seek(0)
    s0.truncate()
    s0.close()
    p.send_now("M18") 
    p.disconnect()

def X_actuator_random(X,F,iteration):
    s0 = open(r"C:\Users\CSMadmin\Desktop\pump_2.0\stop_cache.txt","r+")
    s0.seek(0)
    s0.truncate()
    s0.close()

    findCOM=list(serial.tools.list_ports.grep('1A86:7523')) #find COM of Anet
    global p
    p=printcore(findCOM[0][0],115200) # Connect to the printer  
    while not p.online: time.sleep(0.1)
    
    p.send_now("G91") 
    time.sleep(0.5)
    for k in range (0,int(iteration)):
        rand1=random.randint(2,5)
        rand2=random.randint(1,5)
        
        p.send_now("G1 X" + str(rand1*2.67) + " F" + str(F))
        time.sleep(abs(166.1345*rand1/F))
        if not p.online: break
        
        p.send_now("G1 X" + str(-rand1*2.67) + " F" + str(F))
        time.sleep(abs(166.1345*rand2/F))
        if not p.online: break



    s0 = open(r"C:\Users\CSMadmin\Desktop\pump_2.0\stop_cache.txt","r+")
    s0.seek(0)
    s0.truncate()
    s0.close()
    p.send_now("M18") 
    p.disconnect()





def stop_printer():
    
    while True:
        s = open(r"C:\Users\CSMadmin\Desktop\pump_2.0\stop_cache.txt","r+")
    
        content = s.read()
        time.sleep(1)
        if content=='True':
            s.seek(0)
            s.truncate()
            s.close()
            
            p.send_now("M18")
            p.disconnect()
            break
        s.close()


def main_actuator(X,F,iteration):
    threadA = threading.Thread(target = X_actuator_normal,args=(X,F,iteration))
    threadB = threading.Thread(target = stop_printer)
    threadA.start()
    threadB.start()
    threadA.join()
    threadB.join()



