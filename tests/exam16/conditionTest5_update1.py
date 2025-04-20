from bee.osql.bee_enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2

#update set case 1:
#entity have value (diff case 0)
#donot use condtion setXxx
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    stu.age=11
    
    suidRich = BF.suidRich()
        
    
    # field is null    
    condition = BF.condition()
    # condition.op("remark", Op.eq, None)
    condition.op("addr", Op.eq, None)
    
    orderList = suidRich.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    stu.addr="use new addr"
    stu.remark="bee"
    # updateNum = suidRich.updateBy(stu,condition,"remark")
    # updateNum = suidRich.updateBy(stu,condition,"id")
    updateNum = suidRich.updateBy(stu,condition,"name")
    # updateNum = suidRich.updateBy(stu,condition) # check
    # updateNum = suidRich.updateBy(stu,condition,"")# check
    # updateNum = suidRich.updateBy(stu,condition," ")# check
    print(updateNum)
    # updateBy SQL: update student2 set age = ?, addr = ?, remark = ? where name is null and addr is null
    
    orderList = suidRich.select(stu)
    for one in orderList:
        print(one)    
    
    print("finished")
