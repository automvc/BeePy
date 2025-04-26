from bee.api import Suid

from entity.Test import Test
import MyConfig


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # config = HoneyConfig()
    # config.dbname="mysql"
    
    # orders=Orders(id=1, name="bee")
    orders=Test()
    # orders.id=106
    orders.name="bee12"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    orderList=suid.select(orders)
    print(orderList)
    
    for one in orderList:  
        print(one)  
    
    print("finished")