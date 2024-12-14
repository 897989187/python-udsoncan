import udsoncan
import isotp
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
import json
class serverdemo():
    def __init__(self,
                 interfaces:str,
                 payload:str
                 ) -> None:
        

conn = IsoTPSocketConnection('can0', isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=0x123, txid=0x456))

req = udsoncan.services.ECUReset.make_request(reset_type=1, data=b'\x77\x88\x99')
conn.send(req.get_payload()) 
payload = conn.wait_frame(timeout=1)
response = udsoncan.Response.from_payload(payload)
udsoncan.services.ECUReset.interpret_response(response)
if response.service == service.ECUReset and response.code == Response.Code.PositiveResponse and response.service_data.reset_type_echo == 1:
    print('Success!')
else:
    print('Reset failed')