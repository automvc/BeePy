""" batch insert for student2 """

from bee.api import Suid, SuidRich
from bee.sqllib import BeeSql

import MyConfig
from entity.Student2 import Student2


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    createSql = """
    CREATE TABLE student2 (
    id INTEGER PRIMARY KEY NOT NULL, 
    name VARCHAR(100),  
    age INT,  
    remark VARCHAR(100),  
    addr VARCHAR(100)  
    );  
    """
    
    # beeSql=BeeSql()
    # beeSql.modify(createSql, [])
    
    student0=Student2()
    student0.name = "bee"
    
    student1=Student2()
    student1.name = "bee1"
    student1.addr=""
    student1.age=40
    
    entity_list=[]
    entity_list.append(student0)
    entity_list.append(student1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
