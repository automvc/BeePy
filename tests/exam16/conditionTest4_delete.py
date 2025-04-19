from bee.osql.bee_enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    
    suid = BF.suid()
        
    
    # empty condition    
    # condition = BF.condition()
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one) 
    
    # field is null    
    condition = BF.condition()
    # condition.op("remark", Op.eq, None)
    condition.op("addr", Op.eq, None)
    
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    delNum = suid.delete(stu,condition)
    print(delNum) 
    
    
    
    condition = BF.condition()
    condition.op("name", Op.eq, "黄二")
    
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    ##check do not support
    # condition.groupBy("name")
    # condition.having(FunctionType.MAX, "age", Op.lt, 30)
    # condition.orderBy("name")
    delNum = suid.delete(stu,condition)
    print(delNum)        
       
    
    print("finished")
