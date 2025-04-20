from bee.context import HoneyContext

import MyConfig
from bee.honeyfactory import BF
from bee.osql.bee_enum import LocalType
from bee.osql.cache import CacheUtil
from entity.Orders import Orders
from entity.Orders2 import Orders2


#test cache    
# 虽然同表，但不同entity也不能共缓存 
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    orders=Orders()
    # orders = Test()
    orders.id=1
    orders.name = "bee"
    
    suid = BF.suid()
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
        
    
    orders=Orders()
    # orders = Test()
    orders.id=1
    orders.name = "bee"   
    
    # 虽然同表，但不同entity也不能共缓存 
    
    #test cache    
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
        
        
    # print(CacheUtil._getMap())
    print(HoneyContext._get_storage())
    
    print("finished")
