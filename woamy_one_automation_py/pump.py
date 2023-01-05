import serial
import serial.tools.list_ports as port_
import time
import csv

#message_bytes = bytes.fromhex("020C0023E5000080010000000049") #start
#message_bytes = bytes.fromhex("020C002068000080000000000046") #value to 0
#message_bytes = bytes.fromhex("020C0023E500008002000000004A") #stop


def tohex(val):
    return '{:04X}'.format(val & ((1 << 16)-1))


def pump_control_main(): 
    find_COM=list(port_.grep('A10KDPW2')) #find the port
    #conection to the pump
    pump_UART = serial.Serial(
        port=find_COM[0][0],
        baudrate=38400,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    
    #start the pump
    message_bytes = bytes.fromhex("020C0023E5000080010000000049") 
    pump_UART.write(message_bytes)
    pump_UART.read(14)
    time.sleep(1)
    
    path_cache=r"mem_cache.txt"
    
    while 1:
        time.sleep(1)
        
        #read cache every seconds
        with open(path_cache) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_=[]
            for row in csv_reader:
                line_.append(row)
        
        
        if line_[1][1]=='stop':
            message_bytes = bytes.fromhex("020C002068000000000000000046") #value to 0
            pump_UART.write(message_bytes)
            pump_UART.read(14)
            print('Command sent:', "020C002068000000000000000046")
            time.sleep(1)
            message_bytes = bytes.fromhex("020C0023E500008002000000004A") #stop
            pump_UART.write(message_bytes)
            pump_UART.read(14)
            print('Command sent:', "020C0023E500008002000000004A")
            time.sleep(1)
            break

        elif line_[1][1] and int(line_[1][1])>=0 and int(line_[1][1])<101:
            
            pump_speed=int(line_[1][1])
            pump_speed=int(pump_speed*9.763) #conversion to the manual unit in %
            pump_speed_hex=tohex(pump_speed)
                
            command_speed_hex='020C0020680000'+pump_speed_hex+'0000'

            # xor checksum
            packet_list = [command_speed_hex[i:i+2] for i in range(0, len(command_speed_hex), 2)]
            packet_list_hex = [int(i, 16) for i in packet_list]
            xor = 0
            i = 0
            for i in range(len(packet_list_hex)):
                xor ^= packet_list_hex[i]
            #print('00' + hex(xor)[2:].upper())
            
            speed_command=command_speed_hex + '00' + tohex(xor)
            
            print('Command sent pump:', speed_command)
            message_bytes = bytes.fromhex(speed_command)
            pump_UART.write(message_bytes)
            pump_UART.read(14)

    #csv_file.close()
    pump_UART.close()




