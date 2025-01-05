from bee.api import SuidRich
from test.entity.Orders import Orders

""" batch insert for orders """
if __name__ == '__main__':
    print("start")
    
    orders0=Orders()
    orders0.name = "bee"
    
    orders1=Orders()
    orders1.name = "bee1"
    
    entity_list=[]
    entity_list.append(orders0)
    entity_list.append(orders1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    print("finished")
