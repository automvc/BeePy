from bee.api import Suid, SuidRich
from bee.config import PreConfig

from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    
    #suggest set project root path for it
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    orders=Orders()
    orders.name = "bee"
    orders.id=1
    
    suidRich = SuidRich()
    one = suidRich.select_by_id(orders)
    print(one)
    
    delNum = suidRich.delete_by_id(orders)
    print(delNum)
    
    list_entity = suidRich.select(Orders())
    print(list_entity)
    
    
    print("finished")
