""" batch insert for orders """

from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # createSql = """
    # CREATE TABLE orders (
    # id INTEGER PRIMARY KEY NOT NULL, 
    # name VARCHAR(100),  
    # age INT,  
    # remark VARCHAR(100),  
    # ext VARCHAR(100)  
    # );  
    # """
    
    # beeSql=BeeSql()
    # # beeSql.modify(createSql, [])
    # beeSql.modify(createSql)
    
    
    suidRich = SuidRich()
    suidRich.create_table(Orders, True) # would drop the table first
    
    orders0=Orders()
    orders0.name = "bee"
    orders0.remark="remark test"
    
    orders1=Orders()
    orders1.name = "bee1"
    orders1.remark="remark test1"
    
    entity_list=[]
    entity_list.append(orders0)
    entity_list.append(orders1)
    
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
