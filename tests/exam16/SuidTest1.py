# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid

from bee.osql.bee_enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Orders import Orders


# from bee.config import PreConfig
# from org.teasoft.exam.entity.Test import Test
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    # orders=Orders(id=1, name="bee")
    orders=Orders()
    # orders = Test()
    # orders.id=1
    orders.name = "bee"
    
    suid = BF.suid()
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
        
    condition = BF.condition()  
    condition.op("name", Op.ne, "bee1").op("remark", Op.ne, "new2")
    orderList = suid.select(orders,condition)
    for one in orderList: 
        print(one)
        
        
        
       
    
    print("finished")
