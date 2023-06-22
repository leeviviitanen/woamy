import heating_unit
import time

## Memcached values
defaults = {
    "memcache.address"                  : "127.0.0.1:11211",
    "heatingUnit.0.address"             : "/dev/tty.usbserial-ANZ20BUO",
    "heatingUnit.0.enable"              : 0, 
    "heatingUnit.0.target"              : 0, 
    "heatingUnit.0.pythonImportName"    : "async_heating_unit",

    "conveyorBelt.0.address"             : "/dev/tty.usbserial-ANZ20BUO",
    "conveyorBelt.0.enable"              : 0,
    "conveyorBelt.0.target"              : 0,
    "conveyorBelt.0.pythonImportName"    : "async_conveyor_belt",

    "pump.0.address"             : "/dev/tty.usbserial-ANZ20BUO",
    "pump.0.enable"              : 0,
    "pump.0.target"              : 0,
    "pump.0.pythonImportName"    : "async_pump",

    "foamerAir.0.address"             : "/dev/tty.usbserial-ANZ20BUO",
    "foamerAir.0.enable"              : 0,
    "foamerAir.0.target"              : 0,
    "foamerAir.0.pythonImportName"    : "async_foamer_air",
    "listOfDevices"                     : ["heatingUnit_0", "conveyorBelt_0", "pump_0", "foamerAir_0"]
    }





heat1 = heating_unit.HeatingUnit("/dev/tty.usbserial-ANZ20BUO")
print(heat1.get_temperature())

for ind in range(22):
    current_temperature = heat1.get_temperature()

    print(current_temperature)
    if current_temperature < 65.0:
        heat1.heater_switch(True)
    else:
        heat1.heater_switch(False)

    time.sleep(1)
    print(heat1.read_message())


heat1.heater_switch(False)
heat1.close_connection()


