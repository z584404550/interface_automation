#coding:utf-8
import logging
import time
import os
class Log(object):
    #封装logging
    def __init__(self,logger=None):
        '''
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        '''

        #创建一个logging
        self.logger =logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        #创建一个handler，用于写入日志文件
        self.log_time=time.strftime("%Y_%m_%d_")
        self.log_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_name=os.path.join(self.log_path,'Log\err.log')

        fh=logging.FileHandler(self.log_name,'encoding=utf-8')
        fh.setLevel(logging.INFO)

        #创建一个handler，用于输出到控制台
        ch=logging.StreamHandler()
        ch.setLevel(logging.INFO)

        #定义handler的输出格式
        formatter=logging.Formatter('[%(asctime)s]%(filename)s->%(funcName)s line:%(lineno)d {%levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #记录日志后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)

        #关闭文件
        fh.close()
        ch.close()

    def getlog(self):
        return self.logger

if __name__ == '__main__':
    logger=Log().getlog()
    logger.info("this is info")
    logger.debug("this is debug")
    logger.error("this is error")
    logger.warning("this is warning")

