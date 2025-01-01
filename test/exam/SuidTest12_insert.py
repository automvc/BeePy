from bee.api import Suid
from test.entity.Test import Test


if __name__ == '__main__':
    print("start")
    
    # config = HoneyConfig()
    # config.dbName="mysql"
    
    # orders=Orders(id=1, name="bee")
    orders=Test()
    orders.id=104
    orders.name="bee"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    orderList=suid.select(orders)
    print(orderList)
    
    for one in orderList:  
        print(one)  
    
    print("finished")