from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # orders=Orders()
    # orders.name = "bee"
    # orders.id=1
    
    suidRich = SuidRich()
    # one = suidRich.select_by_id(orders)  # 1.5.4
    # one = suidRich.select_by_id(Orders,"1")  #1.6.0
    one = suidRich.select_by_id(Orders,1)
    # one = suidRich.select_by_id(Orders,'bee')  #1.6.0
    print(one)
    
    # one = suidRich.select(orders)
    # print(one)
    
    # delNum = suidRich.delete_by_id(orders) # 1.5.4
    # delNum = suidRich.delete_by_id(Orders, 1)  # 1.6.0
    delNum = suidRich.delete_by_id(Orders, 1, 2)  # 1.6.0
    print(delNum)
    
    # list_entity = suidRich.select(Orders())
    # print(list_entity)
    
    
    print("finished")
