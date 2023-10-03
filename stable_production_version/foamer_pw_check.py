from opcua import Client
from opcua import ua
import time
import csv

client = Client("opc.tcp://10.0.0.63:4840")


"""
MES_TO_PLC_air_flow(one)
MES_TO_PLC_head_speed(two)
MES_TO_PLC_pressure_head(three)
MES_TO_PLC_product_flow(four)
MES_TO_PLC_pump_speed(fife)

PLC_TO_MES_flow_air(one)
PLC_TO_MES_head_speed(two)
PLC_To_MES_backpressure_head(three)
PLC_TO_MES_flow_product(four)
PLC_TO_MES_pressure_head(six)
PLC_TO_MES_temperature_head
"""



try:
    client.connect()
    
    for i in range(10):
    
    	head_rpm_value = int(input("Give head head pressure: "))


    	head_rpm_node = client.get_node("ns=4;s=MES_TO_PLC_pressure_head")
    	speed = ua.DataValue(ua.Variant(head_rpm_value, ua.VariantType.Int32))
    	head_rpm_node.set_value(speed)
    	
    
    	#block for reading head rpm value
    	var_speed_head = client.get_node("ns=4;s=PLC_TO_MES_head_speed")
    	pressure_head_result = var_speed_head.get_value()
    	print("Speed Head Rpm is:",pressure_head_result)
    	time.sleep(0.5)
            
            
           

finally:
    
    client.disconnect()
    print("Finished")

