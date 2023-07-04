from opcua import Client
from opcua import ua
import time

client = Client("opc.tcp://10.0.0.63:4840")
#set correct user name at password
client.set_user('woamy')
client.set_password('woamy1_admin')

value_start=0
value_stop=0
pressure_value=0
try:
    client.connect()
    var = client.get_node("ns=4;s=input start stop")
    dv = ua.DataValue(ua.Variant(value_start, ua.VariantType.Float))
    var.set_value(dv)
    print("test")

    client.connect()
    node = client.get_node("ns=4;s=com_friq")
    speed = ua.DataValue(ua.Variant(pressure_value, ua.VariantType.Float))
    node.set_value(speed)
    
    time.sleep(10)
    client.connect()
    var = client.get_node("ns=4;s=input start stop")
    dv = ua.DataValue(ua.Variant(value_stop, ua.VariantType.Float))
    var.set_value(dv)
    print("test")

    #print(claent.get_values_node("ns=4;s=com_friq"))

finally:
    client.disconnect()