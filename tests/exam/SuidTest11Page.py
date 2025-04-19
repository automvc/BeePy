# from org.teasoft.exam.entity.Test import Test
from bee.api import SuidRich

from entity.Test import Test
import MyConfig


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    # config = HoneyConfig()
    # config.dbname="mysql"
    
    # orders=Orders(id=1, name="bee")
    orders=Test()
    # orders.id=1
    orders.name="bee"
    
    suidRich=SuidRich()
    orderList = suidRich.select_paging(orders, 0, 10)
    print(orderList)
    
    for one in orderList:  
        print(one)  
    
    print("finished")
