#-*- conding:utf-8 -*-
'''
定义用例执行的过程
'''
from Common import Opmysql, Request
from Public import Config
import logging,json

operationdb_interface = Opmysql.OperationDbInterface()  # 实例化接口测试数据库操作类
operation_request = Request.RequestInterface()  # 实例化HTTP请求

class ExecteInterfaceCase(object):
    def execte(self,key_config,case_no):
        case_interface = operationdb_interface.select_one("select interface_gateway.gateway_url,interface.interface_url,interface.exe_mode,case_interface.header_interface,case_interface.params_interface,case_interface.data_interface from interface_gateway inner join config_total on interface_gateway.config_id = config_total.id,case_interface inner join interface on case_interface.interface_id = interface.id where config_total.key_config='%s' and case_no='%s'" %(key_config,case_no))
        self.url_gateway=case_interface['data']['gateway_url']
        self.url_interface=case_interface['data']['interface_url']
        self.headerdata=eval(case_interface['data']['header_interface'])
        self.param_interface=case_interface['data']['params_interface']
        self.data_interface=case_interface['data']['data_interface']
        self.type_interface=case_interface['data']['exe_mode']
        self.case_url = self.url_gateway + self.url_interface
        try:
            result_response=operation_request.http_request(interface_url=self.case_url,headerdata=self.headerdata,interface_param=self.param_interface,interface_data=self.data_interface,request_type=self.type_interface)
            return result_response
        except Exception as e:
            logging.basicConfig(filename=config.src_path + '\log\syserror.log', level=logging.DEBUG,format='%(asctime)s %(filenmae)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
if __name__=='__main__':
    Execte=ExecteInterfaceCase()
    result=Execte.execte('test','login_001')
    data=result['data']
    print(json.loads(data))