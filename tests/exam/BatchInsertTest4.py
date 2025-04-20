""" batch insert for student2 """

from bee.api import SuidRich

import MyConfig
# from bee.honeyfactory import BF
from entity.Student3 import Student3


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    
    
    # suidRich=BF.suidRich()
    # suidRich.create_table(Student3,True) # since 1.6.0
    
    student0=Student3()
    student0.name = "bee"
    student0.age=20
    student0.remark= "bee"
    
    student1=Student3()
    student1.name = "bee1"
    student1.addr=""
    student1.age=22
    student1.remark= "bee1"
    
    student2=Student3()
    student2.name = "黄二"
    student2.addr=""
    student2.age=21
    
    student3=Student3()
    student3.name = "张三"
    student3.addr=""
    student3.age=21
    
    
    entity_list=[]
    entity_list.append(student0)
    entity_list.append(student1)
    entity_list.append(student2)
    entity_list.append(student3)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
