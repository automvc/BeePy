from bee.api import SuidRich

import MyConfig
from bee.osql.bee_enum import FunctionType
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    orders=Orders()
    orders.name = "bee"
    # orders.id=1
    
    suidRich = SuidRich()
    # suidRich.delete(Orders())
    list0=suidRich.select(Orders())
    print(list0)
    
    one = suidRich.select_fun(orders,FunctionType.COUNT,"id")
    print(one)
    
    one = suidRich.select_fun(orders,FunctionType.MAX,"id")
    print(one)
    one = suidRich.select_fun(orders,FunctionType.MIN,"id")
    print(one)
    one = suidRich.select_fun(orders,FunctionType.SUM,"id")
    print(one)
    one = suidRich.select_fun(orders,FunctionType.AVG,"id")
    print(one)
    
    one = suidRich.count(orders)
    print(one)
    
    one = suidRich.exist(orders)
    print(one)
    
    # delNum = suidRich.delete_by_id(orders)
    # print(delNum)
    
    # list_entity = suidRich.select(Orders())
    # print(list_entity)
    
    
    print("finished")
