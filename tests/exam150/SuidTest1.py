from bee.api import Suid, SuidRich
from bee.config import PreConfig

from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    
    #suggest set project root path for it
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    orders=Orders()
    orders.name = "bee"
    
    suidRich = SuidRich()
    one = suidRich.select_first(orders) #test 
    
    print(one)
    
    print("finished")
