# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid
from bee.osql.bee_enum import Op

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
    # orderList = suid.select(stu) #test 
    # for one in orderList: 
    #     print(one)
        
    condition = BF.condition()
    condition.op("name", Op.ne, "bee1").between("age", 20, 28)
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one)
        
        
    condition = BF.condition()  
    condition.op("name", Op.ne, "bee1").or_()
    condition.l_parentheses().between("age", 20, 28).r_parentheses()
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one)
        
        
    condition = BF.condition()
    condition.opWithField("name", Op.eq, "remark")
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one)  
        
    # condition = BF.condition()
    # condition.groupBy("name")
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)     
       
    
    print("finished")
