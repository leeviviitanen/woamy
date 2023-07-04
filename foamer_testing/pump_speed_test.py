from opcua import Client
from opcua import ua

client = Client("opc.tcp://10.0.0.53:4840")
client.set_user('woamy')
client.set_password('woamy1_admin')
try:
    client.connect()
    var = client.get_node("ns=4;s=Belt")
    dv = ua.DataValue(ua.Variant(5.0, ua.VariantType.Float))
    var.set_value(dv)
    print("test")

    client.connect()
    node = client.get_node("ns=4;s=com_friq")
    speed = ua.DataValue(ua.Variant(1000, ua.VariantType.Float))
    node.set_value(speed)
    #print(claent.get_values_node("ns=4;s=com_friq"))

finally:
    client.disconnect()