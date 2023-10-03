import asyncio
import numpy as np
from async_conveyor_belt import ConveyorBelt
from pymemcache.client.base import Client
from serial.tools.list_ports import comports



defaults = {
    "memcache.address"                  : "127.0.0.1:11211",
    

    "conveyorBelt.0.address"             : "opc.tcp://10.0.0.53:4840",
    "conveyorBelt.0.enable"              : 0,
    "conveyorBelt.0.target"              : 0,
    "conveyorBelt.0.pythonImportName"    : "async_conveyor_belt",
    "conveyorBelt.0.status"              : 5,

    
    "listOfDevices"                     : ["conveyorBelt_0"]
    }


async def run_machine():

    ## Create objects for each "module"
    #heatingUnit_0 = HeatingUnit(unit_name="heatingUnit.0", memcached_address=mc.get("memcache.address").decode("ascii"))
    conveyorBelt_0 = ConveyorBelt(unit_name="conveyorBelt.0")
    #pump_0 = Pump(unit_name="pump.0", memcached_address=mc.get("memcache.address").decode("ascii"))
    #foamerAir_0 = FoamerAir(unit_name="foamerAir.0", memcached_address=mc.get("memcache.address").decode("ascii"))

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


  
    ## Initialize memcached
    for key, val in defaults.items():
        mc.set(key, val)







    print("start execution")
    asyncio.run(run_machine())


