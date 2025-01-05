from bee.api import Suid, SuidRich
from bee.sqllib import BeeSql
from test.entity.Orders import Orders
from test.entity.Student import Student


# from test.entity.Student import Student
if __name__ == '__main__':
    print("start")
    
    createSql = """
    CREATE TABLE users (  
    id INTEGER PRIMARY KEY NOT NULL, 
    name VARCHAR(100),  
    age INT,  
    remark VARCHAR(255),  
    addr VARCHAR(255)  
    );  
    """
    
    # beeSql=BeeSql()
    # beeSql.modify(createSql, []);
    
    student0=Orders()
    student0.name = "bee"
    
    student1=Orders()
    student1.name = "bee1"
    
    entity_list=[]
    entity_list.append(student0)
    entity_list.append(student1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
