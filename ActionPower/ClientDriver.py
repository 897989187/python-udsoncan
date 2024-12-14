from typing import Callable, Union, List, TypedDict, Dict
import isotp
import json
from can.interfaces.socketcan import SocketcanBus
from udsoncan import Response
from udsoncan import services
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.exceptions import *
from udsoncan.services import *
from udsoncan.typing import ClientConfig
from Common import CommonFunc
from DataStruct import *
import can
# from can.interfaces.socketcan import SocketcanBus
import udsoncan.configs
import sys
import re
globallogger = CommonFunc.InitLogging("Uds.log", "main")
class UdsClient(Client):    

    logger = CommonFunc.InitLogging("Uds.log", "UdsClient")
    ExcuteResult:bool = True
    def __init__(self,
                 trans:TransConfig, # 描述can通讯参数
                 udsconfig:ClientConfig = None,    # 描述uds会话参数
                 ) -> None:
        isotp_params = {
            'stmin': 32,                            # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
            'blocksize': 8,                         # Request the sender to send 8 consecutives frames before sending a new flow control message
            'wftmax': 0,                            # Number of wait frame allowed before triggering an error
            'tx_data_length': 8,                    # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
            # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
            'tx_data_min_length': None,
            'tx_padding': 0,                        # Will pad all transmitted CAN messages with byte 0x00.
            'rx_flowcontrol_timeout': 1000,         # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
            'rx_consecutive_frame_timeout': 1000,   # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
            #  'squash_stmin_requirement': False,      # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
            'max_frame_size': 4095,                 # Limit the size of receive frame.
            'can_fd': False,                        # Does not set the can_fd flag on the output CAN messages
            'bitrate_switch': False,                # Does not set the bitrate_switch flag on the output CAN messages
            'rate_limit_enable': False,             # Disable the rate limiter
            #  'rate_limit_max_bitrate': 1000000,      # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
            'rate_limit_window_size': 0.2,          # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
            'listen_mode': False,                   # Does not use the listen_mode which prevent transmission.
        }
        self.If = trans
        try:
            bus = SocketcanBus(self.If['BusID'])  
            notifier = can.Notifier(bus, [can.Printer()])
            tp_addr = isotp.Address(CommonFunc.TurnStrtoEnum(self.If['FrameType'], isotp.AddressingMode), txid = int(self.If['ResponseID']), rxid = int(self.If['RequestID']))
            stack = isotp.NotifierBasedCanStack(bus=bus, notifier=notifier, address=tp_addr, params=isotp_params) # Network/Transport layer (IsoTP protocol). Register a new listenenr
            conn = PythonIsoTpConnection(stack)# interface between Application and Transport layer

            super().__init__(conn, request_timeout=2)
            
        except Exception as e:
            self.logger.error("Clientinit error {}".format(e))

    def Proc(self, flow:UdsStepModel) -> dict:
        ParmValue:list = flow['ParmValue']
        req: services.SecurityAccess.InterpretedResponse = None
        if flow['FuncName'] == '$10':
            session = int(ParmValue[0], 16)
            req = self.change_session(session)
        elif flow['FuncName'] == '$27':
            level = int(ParmValue[0], 16)
            seed = bytes(ParmValue[1])
            req = self.unlock_security_access(level, seed)
        elif flow['FuncName'] == '$22':
            id = int(ParmValue[0], 16)
            req = self.read_data_by_identifier(id)
        elif flow['FuncName'] == '2E':
            id = int(ParmValue[0], 16)
            value = int(ParmValue[1], 16)
            req = self.write_data_by_identifier(id ,value)
        elif flow['FuncName'] == '$14':
            group = int(ParmValue[0], 16)
            req = self.read_data_by_identifier(group)
        elif flow['FuncName'] == '$19':
            status_mask = int(ParmValue[0], 16)
            req = self.read_data_by_identifier(status_mask)
        elif flow['FuncName'] == '$2F':
            status_mask = int(ParmValue[0], 16)
            req = self.io_control(status_mask)
        else:
            self.logger.error('Wrong FuncName %s', flow['FuncName'])
            return None
        return self.ExcuteAndGenresponse(req)

        # self.essentialfuncptr= {
        # '$10':self.change_session,# newsession: int
        # '$27':self.unlock_security_access, # level, seed_params=bytes()
        # '$22':self.read_data_by_identifier, # Union[int, List[int]]
        # '$2E':self.write_data_by_identifier, #did: int, value: Any
        # '$14':self.clear_dtc, # group: int = 0xFFFFFF
        # '$19':self.get_dtc_by_status_mask, # status_mask: int
        # '$2F':self.io_control # status_mask: int
        # }
        
    def ExcuteAndGenresponse(self, CertainResponse: Union[
                                                        services.DiagnosticSessionControl.InterpretedResponse, 
                                                        services.SecurityAccess.InterpretedResponse,
                                                        services.ReadDataByIdentifier.InterpretedResponse,
                                                        services.WriteDataByIdentifier.InterpretedResponse,
                                                        services.ClearDiagnosticInformation.InterpretedResponse,
                                                        services.ReadDTCInformation.InterpretedResponse,
                                                        services.InputOutputControlByIdentifier.InterpretedResponse
                                                        ]
                                                        ) -> Optional[dict]: 
        Red:dict = {}
        Red['valid'] = CertainResponse.valid
        if(Red['valid'] == False):
            self.ExcuteResult = False

        Red['invalid_reason'] = CertainResponse.invalid_reason
        Red['positive'] = CertainResponse.positive
        Red['data'] = CertainResponse.data
        return Red
   
     
"""
    python3 ClientDriver.py "{"RequestID":"0x0","ResponseID":"0x1","FrameType":"Standard","SendFilled":null}" "{"p2_timeout":"0","ignore_all_zero_dtc":"true"}" "{"9":{"FuncName":"$10","ParmName":["诊断会话类型"],"ParmType":["int"],"ParmValue":["0x00"],"RawRequest":"10 00","ExpectedResponse":"50 00"}}"

"""

# def main(transarg:str, clientarg:str, flowarg:str) -> str:
def main():
    try:
        filename = sys.argv[1]
        globallogger.debug("filename {}".format(filename))
        #regular search
        match = re.search(r'UdsArgs(\d+)\.json', filename)
        if match:
            number = match.group(1)
        else:
            globallogger.error("input file {} not found or wrong format".format(filename))

        with open(filename, 'r', encoding='utf-8') as file:

            data = json.load(file)
            
            # 从JSON数据中解析出三个结构体
            if len(data) != 3:
                globallogger.error("{} have less than 3 args".format(filename))
                return
            
            # 第一部分解析为TransConfig
            trans_config_data = json.loads(data[0])  # 解析JSON字符串
            trans_config = TransConfig(**trans_config_data)

            # 第二部分解析为ClientConfig
            client_config_data = json.loads(data[1])
            client_config = ClientConfig(**client_config_data)

            # 第三部分解析为UdsStepModel
            uds_step_model_data = json.loads(data[2])
            uds_step_model = UdsStepModel(**uds_step_model_data)
    except Exception as e:
        globallogger.error("{} \n trans_config {} client_config {} uds_step_model {}".format(e, trans_config, client_config, uds_step_model))
        return
    #init client
    globallogger.debug("trans_config {} client_config {} uds_step_model {}".format(trans_config, client_config, uds_step_model))
    #init client
    Ucli = UdsClient(trans_config, client_config)
    
    #return entity
    returnentity:Dict[str, Union[bool, int, str]]
    for key,value in uds_step_model.items():
        returnentity[key] = Ucli.Proc(value)
    
    returnvalue = {"OutItem": json.dumps(returnentity), "Result": Ucli.ExcuteResult}
    with open("Udsoutput{}.json".format(number), "w") as f:
        json.dump(returnvalue, f)
    return 

if __name__ == "__main__":
    main()

# testmodule
test_string = '''
{
    "BusType": "Canfd",
    "BusID": "can0",
    "RequestID": 123,
    "ResponseID": 456,
    "FrameType": "Normal_11bits"
}
'''

json_string = '''
{
    "exception_on_negative_response": true,
    "exception_on_invalid_response": false,
    "exception_on_unexpected_response": true,
    "security_algo": null,
    "security_algo_params": null,
    "tolerate_zero_padding": true,
    "ignore_all_zero_dtc": false,
    "dtc_snapshot_did_size": 2,
    "server_address_format": 1,
    "server_memorysize_format": 4,
    "data_identifiers": {},
    "input_output": {},
    "request_timeout": 5.0,
    "p2_timeout": 3.5,
    "p2_star_timeout": 7.0,
    "standard_version": 2,
    "use_server_timing": true,
    "extended_data_size": {"1": 128, "2": 256}
}
'''
testflow = '''
{
  "1": {
    "FuncName": "$10",
    "ParmName": ["newsession"],
    "ParmType": ["int"],
    "ParmValue": ["13"],
    "RawRequest": "",
    "ExpectedResponse": ""
  }
}
'''

main(test_string, json_string, testflow)
# print(test_string)
# b = services.DiagnosticSessionControl.InterpretedResponse
# b.valid = False
# b.invalid_reason = "1111"
# b.data = bytes([65, 66, 67])
# b.positive = True
# print(b)
# a = UdsClient(test_string, json_string)

# c = a.ExcuteAndGenresponse(b)
# print("usingtest")
