import asyncio
from opcua import Client as OpcUaClient
from pymemcache.client.base import Client
from opcua import ua
import time

# ---------------------block for init ports conections--------------------------
class FoamerUnit:
    def __init__(self, unit_name=None, memcached_host=None, memcached_port=None):
        self.unit_name = "opc.tcp://10.0.0.63:4840"
        """
        MES_TO_PLC_air_flow
        MES_TO_PLC_head_speed
        MES_TO_PLC_pressure_head
        MES_TO_PLC_product_flow
        MES_TO_PLC_pump_speed

        PLC_TO_MES_flow_air
        PLC_TO_MES_head_speed
        PLC_To_MES_backpressure_head
        PLC_TO_MES_flow_product
        PLC_TO_MES_pressure_head
        PLC_TO_MES_temperature_head
        """

    # ----------------block for init all connections command--------------------
    async def _init(self):
        try:
            self.opcua_client = OpcUaClient(self.unit_name)  # init opcua_client
            self.opcua_client.connect()
            # here I should put all tags from flexy
            # first all tags for writing
            self.air_flow_w = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_air_flow")
            self.head_speed_w = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_head_speed")
            self.pressure_head_w = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_pressure_head")
            self.product_flow_w = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_product_flow")
            self.pump_speed_w = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_pump_speed")
            # now all tags for reading
            self.flow_air_r = self.opcua_client.get_node("ns=4;s=PLC_TO_MES_flow_air")
            self.head_speed_r = self.opcua_client.get_node("ns=4;s=PLC_TO_MES_head_speed")
            self.pressure_head_r = self.opcua_client.get_node("ns=4;s=PLC_TO_MES_pressure_head")
            self.flow_product_r = self.opcua_client.get_node("ns=4;s=PLC_TO_MES_flow_product")
            self.backpressure_head_r = self.opcua_client.get_node("ns=4;s=PLC_To_MES_backpressure_head")   
            self.temperature_head_r = self.opcua_client.get_node("ns=4;s=PLC_TO_MES_temperature_head")
        # -------------------block for handling errors------------------
        except Exception as e:
            print("Error while connecting:", e)
            raise

    # -----------block for disconnecting update function------------
    async def disconnect(self):
        if self.opcua_client:
            self.opcua_client.disconnect()

    # --------block for update all values
    async def update(self):  # function for updating all values in memcached and input to modbus
        try:
            await self._init()

            while True:
                try:
                    mc = Client("127.0.0.1:11211")
                    # here I should put all vars from mc like ("conveyorBelt.0.status")

                    # vars for the air pressure
                    air_compressure_value = int(round(float(mc.get("foamer.0.Airtarget"))))
                    # vars for the head RPM
                    head_rpm_value = int(round(float(mc.get("foamer.0.HeadRPMtarget"))))
                    # var for pressure head
                    var_pressure_hed_value = int(round(float(mc.get("foamer.0.PressureHeadtarget"))))
                    # vars for product flow
                    var_value_product_flow = int(round(float(mc.get("foamer.0.ProductFlowtarget"))))
                    # vars for the pump rpm
                    pump_speed_value = int(round(float(mc.get("foamer.0.PumpSpeedtarget"))))
                    # var for conveyor belt
                    #---------------------------------------------------------------------------------------
                    #that i have to change beacose in that unit name i have not acsess to var ("conveyorBelt.0.status")


                    if self.opcua_client:


                    #---------------------------------------------------------------------------------------
                        # here I need to check values of mc variables and insert them to flexy
                        # ------------------air flow percentage (% of the product flow)-----------------
                        # block for insert air pressure value
                        air_node = self.air_flow_w
                        flow_proc = ua.DataValue(ua.Variant(air_compressure_value, ua.VariantType.Int32))
                        air_node.set_value(flow_proc)

                        # block for read percentage of the product flow
                        reading_mode_air = self.flow_air_r
                        air_result = reading_mode_air.get_value()
                        print("air flow percentage is:", air_result)
                        time.sleep(0.5)

                        # ------------Speed Head Rpm--------------

                        # block for input value to head rpm node
                        head_rpm_node = self.head_speed_w
                        speed = ua.DataValue(ua.Variant(head_rpm_value, ua.VariantType.Int32))
                        head_rpm_node.set_value(speed)

                        # block for reading head rpm value
                        var_speed_head = self.head_speed_r
                        pressure_head_result = var_speed_head.get_value()
                        print("Speed Head Rpm is:", pressure_head_result)
                        time.sleep(0.5)

                        # ------------------air pressure head-------------
                        pressure_head_node = self.pressure_head_w
                        pressure_head = ua.DataValue(ua.Variant(var_pressure_hed_value, ua.VariantType.Int32))
                        pressure_head_node.set_value(pressure_head)


                        # block for reading head air pressure head
                        node_pressure_head = self.pressure_head_r
                        var_pressure_head_result = node_pressure_head.get_value()
                        print("pump speed is:", var_pressure_head_result)
                        time.sleep(0.5)

                        # -----------------block for product flow kg/h-----------------------
                        # block for input value product flow
                        prod_flow_node = self.product_flow_w
                        speed = ua.DataValue(ua.Variant(var_value_product_flow, ua.VariantType.Int32))
                        prod_flow_node.set_value(speed)

                        # block for read product flow
                        var_flow = self.flow_product_r
                        var_flow_result = var_flow.get_value()
                        print("product flow kg/h is:", var_flow_result)
                        time.sleep(0.5)

                        # ------------------pump speed rpm--------------------
                        # block for input value
                        speed_rpm_node = self.pump_speed_w
                        pump_speed = ua.DataValue(ua.Variant(pump_speed_value, ua.VariantType.Int32))
                        speed_rpm_node.set_value(pump_speed)

                        # block for reading head air pressure head
                        var_pressure_head = self.backpressure_head_r
                        pressure_head_result = var_pressure_head.get_value()
                        print("air pressure head is:", pressure_head_result)
                        time.sleep(0.5)

                        # -----------------temperature-----------------------
                        # block for read temp of former head
                        former_temp = self.temperature_head_r
                        temp_result = former_temp.get_value()
                        print("temperature of former head is:", temp_result)
                        time.sleep(0.5)

                    else:  
                        air_compressure_value = 0.0
                        head_rpm_value = 0.0
                        var_pressure_hed_value = 0.0
                        var_value_product_flow = 0.0
                        pump_speed_value = 0.0

                    # block for catching errors
                    try:
                        test = self.flow_air_r.get_value()
                        print("Air flow in system is:", test)
                    except Exception as e:
                        print("Error while reading air flow:", e)

                except Exception as e:
                    print("Error during update loop:", e)

                await asyncio.sleep(0.5)

        except Exception as e:
            print("Error while initializing:", e)
        finally:
            await self.disconnect()

# block for running conveyor belt
async def main():
    former_unit = FoamerUnit()
    await former_unit.update()

if __name__ == "__main__":
    asyncio.run(main())

