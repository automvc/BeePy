from bee.osql.bee_enum import Op

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2

#update set case 3:
#entity have value(diff 2)
#use condtion where op and setXxx
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    #entity中，非空的属性，声明在whereFields会转到where中，其它非空的属性转在update set
    stu=Student2()
    stu.age=12
    
    suidRich = BF.suidRich()
        
    
      
    condition = BF.condition()
    #condition中过滤条件都会转在where
    condition.op("remark", Op.eq, "")
    condition.op("addr", Op.eq, None)  # filter/where
    
    #使用condition中set开头的方法，都会用在update set
    condition.set("addr", "use new addr")  # update set
    condition.set("remark", None)  # update set remark=null
    
    
    
    orderList = suidRich.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    updateNum = suidRich.updateBy(stu,condition,"name")
    print(updateNum)
# [INFO]  [Bee] sql>>> updateBy SQL: update student2 set age = ? , addr = ?,remark = ? where name is null and remark = ? and addr is null
# [INFO]  [Bee] sql>>> params: [12, 'use new addr', None, '']
    
    orderList = suidRich.select(stu)
    for one in orderList:
        print(one)    
    
    print("finished")
