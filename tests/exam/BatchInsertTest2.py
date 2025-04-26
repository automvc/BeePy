""" batch insert for orders """

from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders

if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    suidRich = SuidRich()
    
    suidRich.create_table(Orders, True)  # notice: would drop the old table
    
    orders0 = Orders()
    orders0.name = "bee"
    
    orders1 = Orders()
    orders1.name = "bee1"
    
    entity_list = []
    entity_list.append(orders0)
    entity_list.append(orders1)
    
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
