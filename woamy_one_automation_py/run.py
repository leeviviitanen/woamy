import pump
import foamer_air
import conveyer_belt
import heater
import threading

def start_foamer():
    foamer_air.pressure_regulator_control_main()
def start_pump():
    pump.pump_control_main()
def start_conveyer_belt():
    conveyer_belt.conveyer_belt_control_main()
def start_heater():
    heater.heater_control_main()

def main():
    threadA=threading.Thread(target=start_foamer)
    threadB=threading.Thread(target=start_pump)
    threadC=threading.Thread(target=start_conveyer_belt)
    threadD=threading.Thread(target=start_heater)
    threadA.start()
    threadB.start()
    threadC.start()
    threadD.start()
    threadA.join()
    threadB.join()
    threadC.join()
    threadD.join()
    

main()









