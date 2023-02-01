import serial
import time


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

    def __init__(self, port_name):

        print("heating unit port name:", port_name)
        self.ser = serial.Serial(port_name, 250000)
        time.sleep(5)
        self.temperature = 0.0
        self.switch = False


    def get_temperature(self):


        ## Read message to empty the buffer
        self.read_message()
        time.sleep(0.1)

        ## Ask for the temperature
        self.ser.write(b'M105\r\n')
        time.sleep(0.1)

        ## Read messsage containing temperature from buffer
        message = self.read_message()
        message_list = message.split(' ')
        for element in message_list:
            if len(element) < 2:
                continue
            elif element[:2] == 'T:':
                self.temperature = float(element[2:])
                break

        return self.temperature


    def heater_switch(self, switch_value):
        """Switch the heater on/off

        Parameters
        ----------
        switch_value: Boolean
            Turn heater on (True) or off (False)
        """

        if switch_value == self.switch:
            return 

        if switch_value:
            self.ser.write(b'M104 S200\r\n')
            self.switch = True
        else:
            self.ser.write(b'M104 S0\r\n')
            self.switch = False

        self.read_message()


    def read_message(self):
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


    def close_connection(self):

        ## Before closeing the connection switch heater off for safety
        self.heater_switch(False)
        self.ser.close()























