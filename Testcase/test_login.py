#-*-coding:utf-8-*-
from Common import Opmysql, Request
import os,pytest,sys,json
sys.path.append(os.getcwd())

operationdb_interface = Opmysql.OperationDbInterface()  # 实例化接口测试数据库操作类
operation_request = Request.RequestInterface()  # 实例化HTTP请求
class Test_login:
    # @pytest.fixture(scope="module")
    def test_login_001(self):
        key_config='test'
        case_no='login_001'
        case_interface = operationdb_interface.select_one("select interface_gateway.gateway_url,interface.interface_url,interface.exe_mode,case_interface.header_interface,case_interface.params_interface,case_interface.data_interface from interface_gateway inner join config_total on interface_gateway.config_id = config_total.id,case_interface inner join interface on case_interface.interface_id = interface.id where config_total.key_config='%s' and case_no='%s'" %(key_config,case_no))
        self.url_gateway=case_interface['data']['gateway_url']
        self.url_interface=case_interface['data']['interface_url']
        self.headerdata=eval(case_interface['data']['header_interface'])
        self.param_interface=case_interface['data']['params_interface']
        self.data_interface=case_interface['data']['data_interface']
        self.type_interface=case_interface['data']['exe_mode']
        self.case_url = self.url_gateway + self.url_interface
        result_response = operation_request.http_request(interface_url=self.case_url, headerdata=self.headerdata,interface_param=self.param_interface,interface_data=self.data_interface,request_type=self.type_interface)
        data=json.loads(result_response['data'])
        assert data['code'] ==0000

if __name__=='__main__':
    pytest.main()