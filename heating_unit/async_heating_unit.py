import serial
import asyncio
from pymemcache.client.base import Client


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
        
        self.ser = serial.Serial(self.mc.get(self.unit_name + ".address").decode("utf-8"), 250000)
        self.temperature = 0.0
        self.target = 0.0
        self.switch = False
        await asyncio.sleep(5)


    async def get_temperature(self):


        ## Read message to empty the buffer
        await self.read_message()
        await asyncio.sleep(0.1)

        ## Ask for the temperature
        self.ser.write(b'M105\r\n')
        await asyncio.sleep(0.1)

        ## Read messsage containing temperature from buffer
        message = await self.read_message()
        message_list = message.split(' ')
        for element in message_list:
            if len(element) < 2:
                continue
            elif element[:2] == 'T:':
                self.temperature = float(element[2:])
                break

        return self.temperature


    async def heater_switch(self, switch_value):
        """Switch the heater on/off

        Parameters
        ----------
        switch_value: Boolean
            Turn heater on (True) or off (False)
        """

        if switch_value == self.switch:
            print("no changes")

        elif switch_value:
            self.ser.write(b'M104 S200\r\n')
            self.switch = True
            print("switching on")
        elif not switch_value:
            self.ser.write(b'M104 S0\r\n')
            self.switch = False
            print("switching off")

        await self.read_message()


    async def read_message(self):
        """Print message from self.ser - usb device

        Returns
        -------
        message: str
            Message read from the buffer of the device
        """


        message_bits = self.ser.inWaiting()
        if message_bits:
            message = self.ser.read(message_bits)
            return message.decode('utf-8')


    async def close_connection(self):

        ## Before closeing the connection switch heater off for safety
        await self.heater_switch(False)
        self.ser.close()

    async def update(self):

        current_t = await self.get_temperature()
        ## Future implement function that checks target from memcached
        target_t = float(self.mc.get(self.unit_name + ".target").decode("utf-8"))
        print("current:", current_t, "target:", target_t)
        if target_t > current_t:
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

















