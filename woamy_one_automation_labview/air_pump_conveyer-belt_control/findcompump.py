import serial,serial.tools.list_ports


def main():
    findCOM=list(serial.tools.list_ports.grep('0403:6001')) #find COM of pump
    return findCOM[0][0]
