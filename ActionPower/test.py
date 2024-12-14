# from udsoncan.connections import SyncAioIsotpConnection
# from udsoncan.client import Client
# import logging

# logging.basicConfig(level=logging.DEBUG)

# conn = SyncAioIsotpConnection(interface="virtual", channel=0, bitrate=500000, rx_id=0x123, tx_id=0x456)
# with Client(conn) as client:
#    with client.suppress_positive_response:
#       client.change_session(3)
#       # ...

import json
from typing import Callable, Union, List, TypedDict, Dict
import sys

class UdsStepModel(TypedDict, total=False):
   FuncName: str
   ParmName: List[str]
   ParmType: List[str]
   ParmValue: List[str]
   RawRequest: str
   ExpectedResponse: str

def main():
   transarg:str =sys.argv[1]
   clientarg:str = sys.argv[2]
   flowarg:str = sys.argv[3]
   print("transarg: {}\n clientarg: {}\n flowarg: {}\n" .format(transarg, clientarg, flowarg))
   flow:Dict[str, UdsStepModel] = json.loads(flowarg)

if __name__ == "__main__":
    main()