
from bee.api import SuidRich
from bee.config import PreConfig

from entity.Orders01 import Orders

if __name__ == '__main__':
    print("start")
    
    #set bee.properties/bee.json config folder
    #config_folder_root_path没有帮拼接sqlite的db地址。
    # PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\PyTest\\resources"
    PreConfig.config_path="E:\\JavaWeb\\eclipse-workspace202312\\PyTest\\resources"
    
    orders=Orders()
    # orders.name = "bee"
    
    suidRich = SuidRich()
    one = suidRich.select(orders) #test 
    
    print(one)
    
    print("finished")
