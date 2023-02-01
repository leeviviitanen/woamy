import asyncio
import serial
import time
from pymemcache.client.base import Client



class ConveyorBelt:

    def __init__(self, unit_name=None, memcached_address=None):

        self.mc_address = memcached_address
        self.unit_name = unit_name

    async def _init(self):

        self.mc = Client(self.mc_address)
        self.ser = serial.Serial(
            self.mc.get(self.unit_name + ".address").decode("ascii"), #COM port of the conveyer belt
            baudrate=115200,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        print(self.ser)
        self.speed = 0.0

        self.ser.reset_input_buffer()
        message_bytes = bytes.fromhex("010600000001480A") 
        self.ser.write(message_bytes)
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
            return message


    #calculate the crc modbus checksum
    async def calc_crc_modbus(self, data):
        crc = 0xFFFF
        for pos in data:
            crc ^= pos 
            for i in range(8):
                if ((crc & 1) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1              
        crc="%04X"%(crc)
        return crc[2:4]+crc[:2]

    #conversion to hex value
    async def tohex(self, val):
        return '{:04X}'.format(val & ((1 << 16)-1))




    async def update(self):
        
        target_speed = self.mc.get(self.unit_name + ".target").decode("ascii")
        speed = self.speed

        if target_speed == "stop":
            message_bytes = bytes.fromhex("01060000000089CA") #stop
            print("Sending: stop")
            self.ser.reset_input_buffer()
            self.ser.write(message_bytes)
            await asyncio.sleep(0.1)
            self.read_message()
            print("Finished: stop")


        else:
        
            cb_speed = int(-10*float(target_speed)) #conversion to frequency Hz, '-' because of the direction
            cb_speed_hex = await self.tohex(cb_speed)
                
            command_speed_hex ='01060001'+ cb_speed_hex

            data = bytearray.fromhex(command_speed_hex)
            crc_checksum = await self.calc_crc_modbus(data)
         
            speed_command = command_speed_hex + crc_checksum
            
            message_bytes = bytes.fromhex(speed_command)
            print("Belt", message_bytes)
            self.ser.reset_input_buffer()
            self.ser.write(message_bytes)
            await asyncio.sleep(0.1)
            print(self.read_message())
            self.speed = float(target_speed)


    async def close_connection(self):

        ## First stop the conveyor belt 
        message_bytes = bytes.fromhex("01060000000089CA") #stop
        self.ser.write(message_bytes)
        await asyncio.sleep(0.1)
        self.read_message()
        self.ser.close()


