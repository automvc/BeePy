from bee.api import SuidRich
from bee.bee_enum import Op, FunctionType
from bee.honeyfactory import BF

import MyConfig
from entity.Student2 import Student2


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    stu=Student2()
    # stu.name='张三'

    condition = BF.condition()
    condition.selectField("name,count(*) as remark") #found one bug
    condition.op("name", Op.ne, "bee1")
    condition.groupBy("name")
    # having(FunctionType.MIN, "field", Op.ge, 60)-->having min(field)>=60
    condition.having(FunctionType.MIN, "age", Op.ge, 21)
    condition.having(FunctionType.MAX, "age", Op.lt, 30)
    condition.orderBy("name")
    
        
    # suidRich = BF.suidRich()    
    suidRich = SuidRich()
    
    List =suidRich.select_paging( stu, 0, 10, "name,age")
    List =suidRich.select_paging( stu, 0, 10)
    for one in List:
        print(one)
       
    
    print("finished")
