import json
from typing import Optional, Any, Union, Dict
from typing_extensions import TypedDict

# 定义 ClientConfig 类
class ClientConfig(TypedDict, total=False):
    exception_on_negative_response: bool
    exception_on_invalid_response: bool
    exception_on_unexpected_response: bool
    security_algo: Optional[Any]  # 假设 SecurityAlgoType 为 Any，如果有确切类型请替换
    security_algo_params: Optional[Any]
    tolerate_zero_padding: bool
    ignore_all_zero_dtc: bool
    dtc_snapshot_did_size: int
    server_address_format: Optional[int]
    server_memorysize_format: Optional[int]
    data_identifiers: Any  # 假设 DIDConfig 为 Any，如果有确切类型请替换
    input_output: Any      # 假设 IOConfig 为 Any，如果有确切类型请替换
    request_timeout: float
    p2_timeout: float
    p2_star_timeout: float
    standard_version: int
    use_server_timing: bool
    logger_name: str
    extended_data_size: Optional[Union[int, Dict[int, int]]]

# JSON 字符串示例
json_string = '''
{
    "exception_on_negative_response": "true",
    "exception_on_invalid_response": "false",
    "exception_on_unexpected_response": "true",
    "security_algo": "null",
    "security_algo_params": "null",
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

# 将 JSON 字符串加载为字典
data = json.loads(json_string)

# 将字典转换为 ClientConfig 类型的对象
client_config: ClientConfig = ClientConfig(**data)

# 输出以验证
print(type(client_config["exception_on_negative_response"]))
