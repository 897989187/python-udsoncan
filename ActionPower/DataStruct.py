from typing import Optional, TypedDict, List
from udsoncan.typing import ClientConfig
# from utils import CommonFunc



# logger = CommonFunc.InitLogging(__name__)

#传输层参数集合
class TransConfig(TypedDict, total = False):
    BusType: Optional[str] = 'Canfd'   # Can/Canfd
    BusID: str # 通道号 can0 can1 can2 can3
    RequestID: str # 服务端ID
    ResponseID: str # 客户端ID
    FrameType: str # 帧类型 Normal_11bits Extended_29bits
    SendFilled:Optional[bytes] = 0xAA #发送填充值
class UdsStepModel(TypedDict, total=False):
    FuncName: str
    ParmName: List[str]
    ParmType: List[str]
    ParmValue: List[str]
    RawRequest: str
    ExpectedResponse: str
#数据描述集合
class ProcessParm(TypedDict, total = False):
    ServerName:str # 会话名称
    RequestData:str # 请求的原始报文
    ResponseEnable:bool = True, # 是否需要回复
    ResponseExpect:str # 期望回复格式
    Endian: str # 大小端 little big

#输入参数集合定义
class UdsClientParm(TypedDict, total = True):
    TransLayer: TransConfig
    ServLayer: ClientConfig


