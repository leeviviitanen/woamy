import asyncio
import numpy as np
from async_heating_unit import HeatingUnit
from async_pump import Pump
from async_conveyor_belt import ConveyorBelt
from async_foamer_air import FoamerAir
from pymemcache.client.base import Client
from serial.tools.list_ports import comports



defaults = {
    "memcache.address"                  : "127.0.0.1:11211",
    "heatingUnit.0.address"             : "/dev/ttyUSB2",
    "heatingUnit.0.enabled"             : 0, 
    "heatingUnit.0.target"              : 0, 
    "heatingUnit.0.value"               : 0, 
    "heatingUnit.0.pythonImportName"    : "async_heating_unit",

    "conveyorBelt.0.address"             : "/dev/ttyUSB0",
    "conveyorBelt.0.enable"              : 0,
    "conveyorBelt.0.target"              : 0,
    "conveyorBelt.0.pythonImportName"    : "async_conveyor_belt",

    "pump.0.address"             : "/dev/ttyUSB1",
    "pump.0.enable"              : 0,
    "pump.0.target"              : 0,
    "pump.0.pythonImportName"    : "async_pump",

    "foamerAir.0.address"             : "T4",
    "foamerAir.0.enable"              : 0,
    "foamerAir.0.target"              : 0,
    "foamerAir.0.pythonImportName"    : "async_foamer_air",
    # "listOfDevices"                     : ["heatingUnit_0"]
    "listOfDevices"                     : ["heatingUnit_0", "conveyorBelt_0", "pump_0", "foamerAir_0"]
    }


async def run_machine():

    ## Create objects for each "module"
    heatingUnit_0 = HeatingUnit(unit_name="heatingUnit.0", memcached_address=mc.get("memcache.address").decode("ascii"))
    conveyorBelt_0 = ConveyorBelt(unit_name="conveyorBelt.0", memcached_address=mc.get("memcache.address").decode("ascii"))
    pump_0 = Pump(unit_name="pump.0", memcached_address=mc.get("memcache.address").decode("ascii"))
    foamerAir_0 = FoamerAir(unit_name="foamerAir.0", memcached_address=mc.get("memcache.address").decode("ascii"))

    ## Initialize objects using concurrency
    oliot = []
    for device in eval(mc.get("listOfDevices").decode("ascii")):
        oliot.append(eval(device))


    coros = [getattr(olio, "_init")() for olio in oliot]
    await asyncio.gather(*coros)

    ## Start the main loop 
    ## On each step run the "update" mehtod of the object
    for ind in range(200000):

        oliot = []
        for device in eval(mc.get("listOfDevices").decode("ascii")):
            oliot.append(eval(device))

        coros = [getattr(olio, "update")() for olio in oliot]
        coros.append(asyncio.sleep(0.5))
        results = await asyncio.gather(*coros)
        ##await asyncio.sleep(1)


    oliot = []
    for device in eval(mc.get("listOfDevices").decode("ascii")):
        oliot.append(eval(device))
    coros = [getattr(olio, "close_connection")() for olio in oliot]
    results = await asyncio.gather(*coros)

if __name__ == "__main__":


    mc_address = defaults["memcache.address"]
    mc = Client(mc_address)


    ## serian numbers
    # Belt port name 'AB0OZ6LF'
    # Pump port name 'A10KDPW2'
    # Heater port name 'ANZ20BUO'
    comport_list = list(comports())
    for comport in comport_list:
        serial_number = comport.serial_number
        print("serial number", serial_number)
        val = comport.device
        if serial_number == 'AB0OZ6LF':
            key = "conveyorBelt.0.address"
            print(key, val)
            defaults[key] = val
        elif serial_number == 'A10KDPW2':
            key = "pump.0.address"
            print(key, val)
            defaults[key] = val
        elif serial_number == 'ANZ20BUO':
            key = "heatingUnit.0.address"
            print(key, val)
            defaults[key] = val
        elif serial_number == None:
            key = "foamerAir.0.address"
            val = "T4"
            print(key, val)
            defaults[key] = val

    ## Initialize memcached
    for key, val in defaults.items():
        mc.set(key, val)







    print("start execution")
    asyncio.run(run_machine())

