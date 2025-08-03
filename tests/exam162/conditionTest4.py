# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid

# from bee.config import PreConfig

import MyConfig
from bee.honeyfactory import BF
from bee.bee_enum import Op, FunctionType
from entity.Student2 import Student2


# from bee.config import PreConfig
# from org.teasoft.exam.entity.Test import Test
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    # stu.name='张三'
    
    # suid = BF.suid()
        
  
        
    condition = BF.condition()
    condition.selectField("name,count(*) as remark") #found one bug
    condition.op("name", Op.ne, "bee1")
    condition.groupBy("name")
    # having(FunctionType.MIN, "field", Op.ge, 60)-->having min(field)>=60
    condition.having(FunctionType.MIN, "age", Op.ge, 21)
    condition.having(FunctionType.MAX, "age", Op.lt, 30)
    condition.orderBy("name")
    
    # orderList = suid.select(stu,condition)
    # for one in orderList: 
    #     print(one)
        
    suidRich = BF.suidRich()    
    # List = suidRich.select(Entity())
    # List = suidRich.select(stu)
    
    List =suidRich.select_paging( stu, 0, 10, "name,age")
    List =suidRich.select_paging( stu, 0, 10)
    for one in List:
        print(one)
       
    
    print("finished")
