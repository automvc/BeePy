""" batch insert for student2 """

from bee.api import SuidRich

import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2

if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # createSql = """
    # CREATE TABLE student2 (
    # id INTEGER PRIMARY KEY NOT NULL, 
    # name VARCHAR(100),  
    # age INT,  
    # remark VARCHAR(100),  
    # addr VARCHAR(100)  
    # );  
    # """
    # preparedSql=BF.preparedSql()
    # preparedSql.modify(createSql, [])
    
    suidRich = BF.suidRich()
    suidRich.create_table(Student2, True)  # since 1.6.0   #notice: would drop the old table
    
    student0 = Student2()
    student0.name = "bee"
    student0.age = 20
    student0.remark = "bee"
    
    student1 = Student2()
    student1.name = "bee1"
    student1.addr = ""
    student1.age = 22
    student1.remark = "bee1"
    
    student2 = Student2()
    student2.name = "黄二"
    student2.addr = ""
    student2.age = 21
    
    student3 = Student2()
    student3.name = "张三"
    student3.addr = ""
    student3.age = 21
    
    entity_list = []
    entity_list.append(student0)
    entity_list.append(student1)
    entity_list.append(student2)
    entity_list.append(student3)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
