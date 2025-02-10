""" batch insert for orders """

from bee.api import SuidRich
from bee.config import PreConfig
from bee.sqllib import BeeSql
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    createSql = """
    CREATE TABLE orders (
    id INTEGER PRIMARY KEY NOT NULL, 
    name VARCHAR(100),  
    age INT,  
    remark VARCHAR(100),  
    ext VARCHAR(100)  
    );  
    """
    
    # beeSql=BeeSql()
    # # beeSql.modify(createSql, [])
    # beeSql.modify(createSql)
    
    orders0=Orders()
    orders0.name = "bee"
    orders0.remark="remark test"
    
    orders1=Orders()
    orders1.name = "bee1"
    orders1.remark="remark test1"
    
    entity_list=[]
    entity_list.append(orders0)
    entity_list.append(orders1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
