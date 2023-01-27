import asyncio
from labjack import ljm
from pymemcache.client.base import Client



class FoamerAir:

    def __init__(self, unit_name=None, memcached_address=None):

        self.mc_address = memcached_address
        self.unit_name = unit_name

    async def _init(self):

        self.mc = Client(self.mc_address)
        self.pressure = 0.

        self.handle = ljm.openS(self.mc.get(self.unit_name + ".address").decode("utf-8"), "ANY", "ANY")  # T4 device, Any connection, Any identifier

            
        # Setup and call eWriteAddress to write a value to the LabJack.
        self.address_w = 1002  # DAC1
        self.address_r = 0  # AIN0
        self.dataType = ljm.constants.FLOAT32



    async def update(self):
        
        
        target_pressure = self.mc.get(self.unit_name + ".target").decode("ascii")
        pressure_value = self.pressure
        
        #condition to stop the air
        if target_pressure == 'stop':
            ljm.eWriteAddress(self.handle, self.address_w, self.dataType, 0)
            return
        
        if float(target_pressure) == pressure_value:
            return
        #sending commands to change the air pressure
        elif target_pressure and float(target_pressure)>=0 and float(target_pressure)<=5:
            
            self.pressure = float(target_pressure)
            ljm.eWriteAddress(self.handle, self.address_w, self.dataType, pressure_value)
            pressure_sensor_value = ljm.eReadAddress(self.handle, self.address_r, self.dataType)
            

    async def close_connection(self):
        # Close handle
        ljm.eWriteAddress(self.handle, self.address_w, self.dataType, 0)
        ljm.close(self.handle)
    
    
