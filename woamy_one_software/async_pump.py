import asyncio
import serial
from pymemcache.client.base import Client



class Pump:

    def __init__(self, unit_name=None, memcached_address=None):

        self.mc_address = memcached_address
        self.unit_name = unit_name

    async def _init(self):

        self.mc = Client(self.mc_address)

        self.ser = serial.Serial(
            self.mc.get(self.unit_name + ".address").decode("utf-8"),
            baudrate=38400,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self.speed = 0.0

        await asyncio.sleep(0.1)
        #start the pump
        message_bytes = bytes.fromhex("020C0023E5000080010000000049") 
        self.ser.write(message_bytes)
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

    async def tohex(self, val):
        return '{:04X}'.format(val & ((1 << 16)-1))


    async def update(self):
        
        
        
        target_speed = self.mc.get(self.unit_name + ".target").decode("utf-8")
        pump_speed = self.speed
        
        
        ## Stop the pump
        if target_speed == 'stop':
            message_bytes = bytes.fromhex("020C002068000000000000000046") #value to 0
            self.ser.write(message_bytes)
            self.read_message()

            message_bytes = bytes.fromhex("020C0023E500008002000000004A") #stop
            self.ser.write(message_bytes)
            self.read_message()
            return

        ## Keep the speed same
        elif float(target_speed) == pump_speed:
            return
    
        ## Change the speed
        elif int(target_speed) and int(target_speed)>=0 and int(target_speed)<101:
            
            pump_speed = int(target_speed)
            pump_speed = int(pump_speed*9.763) #conversion to the manual unit in %
            pump_speed_hex = (await self.tohex(pump_speed))
                
            command_speed_hex = '020C0020680000' + pump_speed_hex + '0000'

            # xor checksum
            packet_list = [command_speed_hex[i:i+2] for i in range(0, len(command_speed_hex), 2)]
            packet_list_hex = [int(i, 16) for i in packet_list]
            xor = 0
            i = 0
            for i in range(len(packet_list_hex)):
                xor ^= packet_list_hex[i]
            #print('00' + hex(xor)[2:].upper())
            
            speed_command=command_speed_hex + '00' + (await self.tohex(xor))
            
            message_bytes = bytes.fromhex(speed_command)
            self.ser.write(message_bytes)
            self.read_message()

    ## If the connection is closed set speed to zero shut down the pump
    async def close_connection(self):

        message_bytes = bytes.fromhex("020C002068000000000000000046") #value to 0
        self.ser.write(message_bytes)
        self.read_message()

        message_bytes = bytes.fromhex("020C0023E500008002000000004A") #stop
        self.ser.write(message_bytes)
        self.read_message()
        self.ser.close()

