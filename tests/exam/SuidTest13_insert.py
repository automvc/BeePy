from bee.api import Suid

import MyConfig
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # config = HoneyConfig()
    # config.dbname="mysql"
    
    # orders=Orders(id=1, name="bee")
    orders=Orders()
    # orders.id=104
    orders.name="bee13"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    orderList=suid.select(orders)
    print(orderList)
    
    for one in orderList:  
        print(one)  
    
    print("finished")