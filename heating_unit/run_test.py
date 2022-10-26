import heating_unit
import time







heat1 = heating_unit.HeatingUnit("/dev/tty.usbserial-ANZ20BUO")
print(heat1.get_temperature())

for ind in range(1200):
    current_temperature = heat1.get_temperature()

    print(current_temperature)
    if current_temperature < 50.0:
        heat1.heater_switch(True)
    else:
        heat1.heater_switch(False)

    time.sleep(1)
    print(heat1.read_message())


heat1.heater_switch(False)
heat1.close_connection()


