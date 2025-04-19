from bee.api import SuidRich

import MyConfig
from entity.Orders_202501 import Orders_202501


# test unique,index_normal
if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    suidRich = SuidRich()
    suidRich.create_table(Orders_202501,True)
    
    suidRich.unique(Orders_202501, "name")
    # suidRich.index_normal(Orders_202501, "name*")
    # suidRich.index_normal(Orders_202501, "name#")
    # suidRich.index_normal(Orders_202501, "name","name#")
    
    suidRich.drop_index(Orders_202501, "uie_orders_202501_name")
    
    entity=Orders_202501()
    entity.name="2025"
    entity.remark="test create table"
    suidRich.insert(entity)
    suidRich.insert(entity)
    
    one = suidRich.select(Orders_202501())
    print(one)
    
    
