# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid

# from bee.config import PreConfig
from bee.osql.enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2


# from bee.config import PreConfig
# from org.teasoft.exam.entity.Test import Test
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    # stu.name='张三'
    
    suid = BF.suid()
        
    
    # empty condition    
    condition = BF.condition()
    orderList = suid.select2(stu,condition)
    for one in orderList: 
        print(one) 
    
    # field is null    
    condition = BF.condition()
    # condition.op("remark", Op.eq, None)
    condition.op("addr", Op.eq, None)
    orderList = suid.select2(stu,condition)
    for one in orderList: 
        print(one)         
       
    
    print("finished")
