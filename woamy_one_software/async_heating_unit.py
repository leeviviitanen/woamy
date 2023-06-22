import serial
import time
import asyncio
import serial_asyncio
from pymemcache.client.base import Client
from serial.tools.list_ports import comports

class HeatingUnit:
    """
    A class for Woamy machine heating unit control

    ...

    Attributes
    ----------
    temperature: float
        Temperature measured inside the heater unit
    target_temperature: float
        Desired temperature set by user (default 0.0)
    ser: Serial() object
        Serial object for the usb serial port cotrol
    switch: Boolean
        Describes if heater is on (True) or off (False)

    Methods
    -------
    get_temperature()
        Measures the temperature inside unit. Returns and updates the value
    heater_switch(value)
        Switches the heating lamp on or off
    """

    def __init__(self, unit_name=None, memcached_address=None):

        self.mc_address = memcached_address
        self.unit_name = unit_name

    async def _init(self):
        self.mc = Client(self.mc_address)

        comport_list = list(comports())
        for comport in comport_list:
            serial_number = comport.serial_number
            val = comport.device
            if serial_number == 'ANZ20BUO':
                key = "heatingUnit.0.address"
                break

        self.mc.set(key, val)

        
        print(self.mc.get(self.unit_name + ".address").decode("utf-8"))
        self.ser = serial.Serial(self.mc.get(self.unit_name + ".address").decode("utf-8"), 250000)
        # self.reader, self.writer = await serial_asyncio.open_serial_connection(self.mc.get(self.unit_name + ".address").decode("utf-8"), baudrate=250000)
        self.temperature = 0.0
        self.target = 0.0
        self.switch = False
        await asyncio.sleep(1)


    async def get_temperature(self):


        ## Read message to empty the buffer
        # await self.read_message()

        ## Ask for the temperature
        self.ser.write(b'M105\r\n')

        ## Read messsage containing temperature from buffer
        await asyncio.sleep(0.1)
        message = self.read_message()
        try: 
            message_list = message.split(' ')
            for element in message_list:
                if len(element) < 2:
                    continue
                elif element[:2] == 'T:':
                    self.temperature = float(element[2:])
                    break
        except:
            pass

        return self.temperature


    async def heater_switch(self, switch_value):
        """Switch the heater on/off

        Parameters
        ----------
        switch_value: Boolean
            Turn heater on (True) or off (False)
        """

        if switch_value == self.switch:
            pass

        elif switch_value:
            self.ser.write(b'M104 S200\r\n')
            self.switch = True
            print("switching on")
        elif not switch_value:
            self.ser.write(b'M104 S0\r\n')
            self.switch = False
            print("switching off")

        await asyncio.sleep(0.1)
        self.read_message()


    def read_message(self):
        """Print message from self.ser - usb device

        Returns
        -------
        message: str
            Message read from the buffer of the device
        """


        message_bits = self.ser.in_waiting
        if message_bits:
            message = self.ser.read(message_bits)
            return message.decode('utf-8')


    async def close_connection(self):

        ## Before closeing the connection switch heater off for safety
        await self.heater_switch(False)
        self.ser.close()

    async def update(self):
        """Update values between memcached and device or try to re-connect device if the device is not enabled.

        """

        enabled = int(self.mc.get(self.unit_name + ".enabled").decode("utf-8"))
        if enabled:
            try: 
                await self.update_temperature()
            except:
                self.mc.set(self.unit_name + ".enabled", 0)

        elif not enabled:
            try:
                await self._init()
                self.mc.set(self.unit_name + ".enabled", 1)
            except:
                print("Unable to find", self.unit_name)
                print("Check connection of", self.unit_name)
                self.mc.set(self.unit_name + ".enabled", 0)


    async def update_temperature(self):

        current_t = await self.get_temperature()
        self.mc.set(self.unit_name + ".value", current_t)
        ## Future implement function that checks target from memcached
        target_t = self.mc.get(self.unit_name + ".target").decode("utf-8")
        print("current:", current_t, "target:", target_t)
        if target_t == "stop":
            await self.heater_switch(False)
        elif float(target_t) > current_t:
            await self.heater_switch(True)
        else:
            await self.heater_switch(False)

        ## Update heater status to memcache
        ## Update the current temperature to memcache





"""
async def run_heater():

    heat1 = heating_unit.HeatingUnit("/dev/tty.usbserial-ANZ20BUO")
    await heat1._init()
    for ind in range(30):
        await asyncio.gather(
                heat1.update()
                )

if __name__ == "__main__":


    asyncio.run(run_heater())
"""

