#-*- coding:utf-8 -*-
#__author__='大婶N72'
'''
定义导出数据库表数据到Excel的类。如果要是Excel 2007版本，则使用openpyxl模块
1.用init方法初始化获取配置文件数据
2.export2excel为主方法
'''
from xlrd import open_workbook
# from openpyxl import load_workbook
from xlutils.copy import copy
import logging,datetime
from Common import Opmysql
from Public import Config
operation_db= Opmysql.OperationDbInterface(link_type=1)#实例化自动化测试数据库操作类
class AnalyseData(object):
    '''
    定义对接口测试数据进行分析的类，包含的方法有:
    1.导出测试数据到excel中
    '''
    def __init__(self):
        self.field=config.field_excel#初始化配置文件
    #定义导出指定数据到Excel中
    def export2excel(self,names_export):
        '''
        :param names_export: 待导出的接口名称，列表形式数据
        :return:
        '''
        counts_export=len(names_export)#导出总数
        fail_export=[]#导出失败接口名列表
        try:
            src=open_workbook(config.src_path +'/report/report_module.xls', formatting_info=True)
            # src=load_workbook(config.src_path + '/report/report_module.xlsx')
            destination=copy(src)
            dt=datetime.datetime.now().strftime("%Y%m%d%H%M%S")#当前时间戳
            filepath=config.src_path+'/report/'+str(dt)+'.xls'
            destination.save(filepath)#保存模板表格到新的目录下
            for name_interface in names_export:
                cases_interface=operation_db.select_all("select * from case_interface where case_status=1 and name_interface='%s'" %(name_interface))#获取指定接口的测试用例数据
                if len(cases_interface['data'])!=0 and cases_interface['code']=='0000':
                    src=open_workbook(filepath,formatting_info=True)
                    # src=load_workbook(filepath)
                    destination=copy(src)
                    sheet=destination.add_sheet(name_interface,cell_overwrite_ok=True)
                    # destination.save(filepath)
                    for col in range (0,len(self.field)):
                        sheet.write(0,col,self.field[col])#获取并写入数据段信息到sheet
                    for row in range (1,len(cases_interface['data'])+1):
                        for col in range (0,len(self.field)):
                            sheet.write(row,col,'%s' %cases_interface['data'][row-1][col])#写数据到对应Excel表中
                    destination.save(filepath)
                elif len(cases_interface['data'])==0 and cases_interface['code']=='0000':
                    fail_export.append(name_interface)
                else:
                    fail_export.append(name_interface)
            result = {'code': '0000', 'message': '导出总数：%s，失败数：%s' % (counts_export, len(fail_export)),'data': fail_export}
        except Exception as error: #记录日志到log.txt文件
            result={'code':'9999','message':'导出总数：%s，失败数：%s' %(counts_export,len(fail_export)), 'data':fail_export}
            logging.basicConfig(filename=config.src_path + '\log\syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger=logging.getLogger(__name__)
            logger.exception(error)
        return result
if __name__=='__main__':
    names_export=operation_db.select_one("select value_config from config_total where status=1 and key_config='name_export'")#获取导出的接口数据元祖
    print(names_export)
    if names_export['code']=='0000':#判断查询结果
        temp_export=eval(names_export['data'][0])#获取查询数据，并将其转换成字典
        print(temp_export)
        test_analyse_data=AnalyseData()
        result_export=test_analyse_data.export2excel(temp_export)#导出结果
        print(result_export)
    else:
        print('获取导出接口集失败')
