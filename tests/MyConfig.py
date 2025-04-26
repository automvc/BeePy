# import sys
from bee.config import PreConfig, HoneyConfig


def init():

    # python_version = sys.version  # 获取当前 Python 版本 
    # py_version=f'Current Python version: {python_version}' 
    # print(py_version)
        
    #TODO change to your config file path
    PreConfig.config_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\resources"
    
    HoneyConfig() # how to call first time