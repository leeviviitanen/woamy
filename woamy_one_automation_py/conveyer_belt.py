import serial
import serial.tools.list_ports as port_
import time
import csv

#message_bytes = bytes.fromhex("010600000001480A") #start
#message_bytes = bytes.fromhex("010600010000D80A") #value to 0
#message_bytes = bytes.fromhex("01060000000089CA") #stop

#calculate the crc modbus checksum
def calc_crc_modbus(data):
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
def tohex(val):
    return '{:04X}'.format(val & ((1 << 16)-1))



def conveyer_belt_control_main(): 
    #conection to the conveyer belt
    find_COM=list(port_.grep('AB0OZ6LF')) #find the port
    cb_UART = serial.Serial(
        port= find_COM[0][0], #COM port of the conveyer belt
        baudrate=115200,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    
    #start the conveyer belt
    message_bytes = bytes.fromhex("010600000001480A") 
    cb_UART.write(message_bytes)
    time.sleep(1)
    cb_UART.read(8)

    #path of the memory cache
    path_cache=r"mem_cache.txt"
    
    while 1:
        
        #read cache every seconds
        with open(path_cache) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_=[]
            for row in csv_reader:
                line_.append(row)
        
        
        if line_[1][2]=='stop':
            message_bytes = bytes.fromhex("01060000000089CA") #stop
            cb_UART.write(message_bytes)
            time.sleep(1)
            cb_UART.read(8)

            break

        elif line_[1][2]:
            
            cb_speed= int(-10*float(line_[1][2])) #conversion to frequency Hz, '-' because of the direction
            cb_speed_hex=tohex(cb_speed)
                
            command_speed_hex='01060001'+ cb_speed_hex

            data = bytearray.fromhex(command_speed_hex)
            crc_checksum = calc_crc_modbus(data)
         
            speed_command = command_speed_hex + crc_checksum
            
            print('Command sent cb:', speed_command)
            message_bytes = bytes.fromhex(speed_command)
            cb_UART.write(message_bytes)
            time.sleep(1)
            cb_UART.read(8)

    #csv_file.close()
    cb_UART.close()
