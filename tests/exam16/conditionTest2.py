from bee.osql.bee_enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    # stu.name='张三'
    
    suid = BF.suid()
        
    
    # empty condition    
    condition = BF.condition()
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    # field is null    
    condition = BF.condition()
    # condition.op("remark", Op.eq, None)
    condition.op("addr", Op.eq, None)
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one)         
       
    
    print("finished")
