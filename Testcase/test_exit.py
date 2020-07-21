#-*-coding:utf-8-*-
from Common import Opmysql, Request
import os,pytest,sys,json
sys.path.append(os.getcwd())

operationdb_interface = Opmysql.OperationDbInterface()  # 实例化接口测试数据库操作类
operation_request = Request.RequestInterface()  # 实例化HTTP请求

@pytest.fixture(scope="module")
def login():
    key_config = 'test'
    case_no = 'login_001'
    case_interface = operationdb_interface.select_one( "select interface_gateway.gateway_url,interface.interface_url,interface.exe_mode,case_interface.header_interface,case_interface.params_interface,case_interface.data_interface from interface_gateway inner join config_total on interface_gateway.config_id = config_total.id,case_interface inner join interface on case_interface.interface_id = interface.id where config_total.key_config='%s' and case_no='%s'" % (key_config, case_no))
    url_gateway = case_interface['data']['gateway_url']
    url_interface = case_interface['data']['interface_url']
    headerdata = eval(case_interface['data']['header_interface'])
    param_interface = case_interface['data']['params_interface']
    data_interface = case_interface['data']['data_interface']
    type_interface = case_interface['data']['exe_mode']
    case_url = url_gateway + url_interface
    result_response = operation_request.http_request(interface_url=case_url, headerdata=headerdata,interface_param=param_interface,interface_data=data_interface,request_type=type_interface)
    data = json.loads(result_response['data'])

    tokenId=data['data']['tokenId']
    return tokenId
class Test_exit:
    def test_exit_001(self,login):
        key_config = 'test'
        case_no = 'exit_001'
        case_interface = operationdb_interface.select_one("select interface_gateway.gateway_url,interface.interface_url,interface.exe_mode,case_interface.header_interface,case_interface.params_interface,case_interface.data_interface from interface_gateway inner join config_total on interface_gateway.config_id = config_total.id,case_interface inner join interface on case_interface.interface_id = interface.id where config_total.key_config='%s' and case_no='%s'" % (key_config, case_no))
        print(case_interface)
        url_gateway = case_interface['data']['gateway_url']
        url_interface = case_interface['data']['interface_url']
        headerdata = eval(case_interface['data']['header_interface'])
        data_interface = json.dumps({"authorization":login})
        print(data_interface)
        param_interface = case_interface['data']['params_interface']
        # data_interface = case_interface['data']['data_interface']
        type_interface = case_interface['data']['exe_mode']
        case_url = url_gateway + url_interface
        result_response = operation_request.http_request(interface_url=case_url, headerdata=headerdata,interface_param=param_interface, interface_data=data_interface,request_type=type_interface)
        data = json.loads(result_response['data'])
        print(data)
        assert json.loads(result_response['data'])["code"]==0
if __name__=='__main__':
    pytest.main()