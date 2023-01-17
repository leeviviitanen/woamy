import asyncio
import numpy as np
from async_heating_unit import HeatingUnit
from async_pump import Pump
from async_conveyor_belt import ConveyorBelt
from async_foamer_air import FoamerAir
from pymemcache.client.base import Client

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


async def run_machine():

    ## Create objects for each "module"
    heatingUnit_0 = HeatingUnit(unit_name="heatingUnit.0", memcached_address=mc.get("memcache.address").decode("utf-8"))
    conveyorBelt_0 = conveyorBelt(unit_name="conveyorBelt.0", memcached_address=mc.get("memcache.address").decode("utf-8"))
    pump_0 = Pump(unit_name="pump.0", memcached_address=mc.get("memcache.address").decode("utf-8"))
    foamerAir_0 = FoamerAir(unit_name="foamerAir.0", memcached_address=mc.get("memcache.address").decode("utf-8"))

    ## Initialize objects using concurrency
    oliot = []
    for device in eval(mc.get("listOfDevices").decode("ascii")):
        oliot.append(eval(device))


    coros = [getattr(olio, "_init")() for olio in oliot]
    await asyncio.gather(*coros)

    ## Start the main loop 
    ## On each step run the "update" mehtod of the object
    for ind in range(50):

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

    ## Initialize memcached
    for key, val in defaults.items():
        mc.set(key, val)

    



    print("start execution")
    asyncio.run(run_machine())

