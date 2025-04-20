# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid

# from bee.config import PreConfig

import MyConfig
from bee.honeyfactory import BF
from bee.osql.bee_enum import Op, FunctionType
from entity.Student2 import Student2


# from bee.config import PreConfig
# from org.teasoft.exam.entity.Test import Test
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    # stu.name='张三'
    
    suid = BF.suid()
        
    # condition = BF.condition()
    # condition.op("name", Op.ne, "bee1").between("age", 20, 28)
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)
    #
    #
    # condition = BF.condition()  
    # condition.op("name", Op.ne, "bee1").or_()
    # condition.l_parentheses().between("age", 20, 28).r_parentheses()
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)
    #
    #
    # condition = BF.condition()
    # condition.opWithField("name", Op.eq, "remark")
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)  
    
    # PreConfig.sql_key_word_case="upper"
        
    condition = BF.condition()
    condition.selectField("name,count(*) as remark")
    condition.op("name", Op.ne, "bee1")
    condition.groupBy("name")
    # having(FunctionType.MIN, "field", Op.ge, 60)-->having min(field)>=60
    condition.having(FunctionType.MIN, "age", Op.ge, 21)
    condition.having(FunctionType.MAX, "age", Op.lt, 30)
    condition.orderBy("name")
    # condition.orderBy2("age",OrderType.DESC)
    orderList = suid.select(stu,condition)
    for one in orderList: 
        print(one)
        
        
    # condition = BF.condition()
    # condition.groupBy("name")
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)          
       
    
    print("finished")
