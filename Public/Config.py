# -*- coding: UTF-8 -*-
from configparser import ConfigParser
import os

config = ConfigParser()
conf_path = os.path.dirname(os.path.realpath(__file__)) + "\config.ini"
print(conf_path)
config.read(conf_path, encoding="utf-8")
print(config.sections())

# class config(object):
#
#     # path
#     path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
#
#     def __init__(self):
#         """
#         初始化
#         """
#         self.config=ConfigParser()
#         a=self.config.read('config.ini')
#         return a
#
# if __name__=='__main__':
#     config=config()
