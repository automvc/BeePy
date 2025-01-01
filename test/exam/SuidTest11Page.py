# from org.teasoft.exam.entity.Test import Test
from bee.api import Suid
from test.entity.Test import Test


if __name__ == '__main__':
    print("start")
    
    # config = HoneyConfig()
    # config.dbName="mysql"
    
    # orders=Orders(id=1, name="bee")
    orders=Test()
    # orders.id=1
    orders.name="bee"
    
    suid=Suid()
    orderList = suid.select_paging(orders, 0, 10)
    print(orderList)
    
    for one in orderList:  
        print(one)  
    
    print("finished")
