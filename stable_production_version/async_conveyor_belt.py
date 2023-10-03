import asyncio
from opcua import Client as OpcUaClient
from pymemcache.client.base import Client
from opcua import ua
from pymemcache.client.base import Client as mc
#---------------------block for init ports conections--------------------------
class ConveyorBelt:
    def __init__(self, unit_name=None, memcached_host=None, memcached_port=None):
        self.unit_name = unit_name or "opc.tcp://10.0.0.53:4840"
        self.memcached_host = memcached_host or 'localhost'
        self.memcached_port = memcached_port or 11211
    #----------------block for init all connections command--------------------
    async def _init(self):
        try:
            self.opcua_client = OpcUaClient(self.unit_name)
            self.opcua_client.set_user('woamy')
            self.opcua_client.set_password('woamy1_admin')
            self.opcua_client.connect()
            self.var = self.opcua_client.get_node("ns=4;s=Belt")
            self.address_w = self.opcua_client.get_node("ns=4;s=com_friq")
            self.address_r = self.opcua_client.get_node("ns=4;s=Operation_speed_W")
        #-------------------block for handling errors------------------
        except Exception as e:
            print("Error while connecting:", e)
            raise
            
            
            
    #-----------block for disconnecting update function------------
    async def disconnect(self):
        if self.opcua_client:
            self.opcua_client.disconnect()
    #--------block for update all values 
    async def update(self):#function for ubdating all values in memcached and input to motbus
        try:
            await self._init()
            
            while True:
                try:
                    mc = Client("127.0.0.1:11211")
                    start_stop = 5.0 if float(mc.get("conveyorBelt.0.status") or 5) == 5.0 else 1.0#chek mc if value is 5 put 0.5 adervase 1.0
                    dv = ua.DataValue(ua.Variant(start_stop, ua.VariantType.Float))#create var were opc ua input input start_stop  
                    self.var.set_value(dv)#setting value to conveer belt
                    target_speed = 0.0#init var and insert value 0.0

                    if start_stop == 1.0:#if conveer move 
                        target_speed = float(mc.get("conveyorBelt.0.target")) * 40#then tooke value from mc *40 suitable for conveer belt
                        speed_value = ua.DataValue(ua.Variant(target_speed, ua.VariantType.Float))#create var were opc ua input target_speed
                        self.address_w.set_value(speed_value)#setting speed value to conveer belt
                    else:#if  conveer belt does not move 
                        target_speed = 0.0#then speed is 00

                    
                    #block for caching errors
                    try:
                        test = self.address_r.get_value()
                        print("Conveyor belt speed:", test)
                    except Exception as e:
                        print("Error while reading conveyor belt speed:", e)

                except Exception as e:
                    print("Error during update loop:", e)

                await asyncio.sleep(0.5)

        except Exception as e:
            print("Error while initializing:", e)
        finally:
            await self.disconnect()
#block for running conveer belt 
async def main():
    conveyor_belt = ConveyorBelt()
    await conveyor_belt.update()

if __name__ == "__main__":
    asyncio.run(main())


    
