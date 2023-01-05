import sys
sys.path.append("../heating_unit")
import heating_unit

import serial
import serial.tools.list_ports as port_
import time
import csv





def heater_control_main():


    ## Get the correct port for the heating unit
    find_COM=list(port_.grep('ANZ20BUO'))
    port= find_COM[0][0]

    ## Open connection to the heating unit and switch off for safety
    heat1 = heating_unit.HeatingUnit(port)
    heat1.heater_switch(False)
    

    ## Parameter file
    path_cache=r"mem_cache.txt"


    ## Start the main loop
    while 1:
        
        ## Read the desired temperatuer from cache file ([1][4])
        with open(path_cache) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_=[]
            for row in csv_reader:
                line_.append(row)





        ## Turn the heater off and wait
        if line_[1][3] == "stop":
            current_temperature = heat1.get_temperature()
            heat1.heater_switch(False)
            print("Heater Off,  Target T: Stopped , Current T: %1.2f C" %current_temperature)
            time.sleep(1)
            break
            



        else:
            current_temperature = heat1.get_temperature()

            if current_temperature < float(line_[1][3]):
                heat1.heater_switch(True)
                print("Heater On,  Target T: %1.2f C, Current T: %1.2f C" %(float(line_[1][3]), current_temperature))
            else:
                heat1.heater_switch(False)
                print("Heater off, Target T: %1.2f C, Current T: %1.2f C" %(float(line_[1][3]), current_temperature))

        time.sleep(1)
        heat1.read_message()


    heat1.heater_switch(False)
    heat1.close_connection()




