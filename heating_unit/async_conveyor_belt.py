import asyncio
import serial



class ConveyorBelt:

    def __init__(self, unit_name=None, memcached_address=None):

        self.mc_address = memcached_address
        self.unit_name = unit_name

    async def _init(self):

        self.mc = Client(self.mc_address)
        self.ser = serial.Serial(self.mc.get(self.unit_name + ".address").decode("utf-8"), 250000)
        self.speed = 0.0



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
        
        target_speed = self.mc.get(self.unit_name + ".target").decode("utf-8")
        speed = self.speed

        if target_speed == "stop".decode("utf-8"):
            message_bytes = bytes.fromhex("01060000000089CA") #stop
            self.ser.write(message_bytes)
            await asyncio.sleep(0.5)
            self.ser.read(8)
            return

        elif float(target_speed) == speed:
            await asyncio.sleep(0.5)
            return

        else:
        
            cb_speed = int(-10*float(target_speed)) #conversion to frequency Hz, '-' because of the direction
            cb_speed_hex = await tohex(cb_speed)
                
            command_speed_hex ='01060001'+ cb_speed_hex

            data = bytearray.fromhex(command_speed_hex)
            crc_checksum = await calc_crc_modbus(data)
         
            speed_command = command_speed_hex + crc_checksum
            
            message_bytes = bytes.fromhex(speed_command)
            self.ser.write(message_bytes)
            await asyncio.sleep(0.5)
            self.ser.read(8)
            self.speed = float(target_speed)


    async def close_connection(self):

        ## First stop the conveyor belt 
        message_bytes = bytes.fromhex("01060000000089CA") #stop
        self.ser.write(message_bytes)
        await asyncio.sleep(0.5)
        self.ser.read(8)
        self.ser.close()


