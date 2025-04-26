from bee.api import SuidRich

import MyConfig
from entity.Orders_202501 import Orders_202501


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    suidRich = SuidRich()
    # suidRich.create_table(Orders_202501)
    suidRich.create_table(Orders_202501, True)
    
    # entity=Orders_202501()
    # entity.name="2025"
    # entity.remark="test create table"
    # suidRich.insert(entity)
    
    one = suidRich.select(Orders_202501())
    print(one)
    
    
