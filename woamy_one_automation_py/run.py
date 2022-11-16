import pump
import foamer_air
import conveyer_belt
import threading

def start_foamer():
    foamer_air.pressure_regulator_control_main()
def start_pump():
    pump.pump_control_main()
def start_conveyer_belt():
    conveyer_belt.conveyer_belt_control_main()

def main():
    threadA=threading.Thread(target=start_foamer)
    threadB=threading.Thread(target=start_pump)
    threadC=threading.Thread(target=start_conveyer_belt)
    threadA.start()
    threadB.start()
    threadC.start()
    threadA.join()
    threadB.join()
    threadC.join()
    

main()









