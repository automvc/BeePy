""" batch insert for orders """

from bee.api import Suid, SuidRich

import MyConfig
from entity.Orders import Orders
from entity.Orders3 import Orders3


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # select record
    suid=Suid()
    orderList=suid.select(Orders()) #select all
    
    #insert    
    orders=Orders()
    orders.id=104
    orders.name="bee3"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    #update/delete
    orders=Orders3()
    orders.name="bee130"
    orders.ext="aaa"  #实体没有字段，会被忽略。出于安全考虑
    orders.id=104
    
    suid = Suid()
    n1= suid.update(orders)
    n2= suid.delete(orders)
    print(n1)
    print(n2)
    
    print("finished")
