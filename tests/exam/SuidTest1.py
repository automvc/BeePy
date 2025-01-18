# from org.teasoft.exam.entity.Orders import Orders
# from bee.api import Suid
from bee.api import Suid
from entity.Orders import Orders


# from org.teasoft.exam.entity.Test import Test
if __name__ == '__main__':
    print("start")
    
    # Version.printversion()
    
    # orders=Orders(id=1, name="bee")
    orders=Orders()
    # orders = Test()
    # orders.id=1
    orders.name = "bee"
    
    suid = Suid()
    orderList = suid.select(orders) #test 
    orderList = suid.select(orders)
    # print(orderList)
    
    for one in orderList: 
        print(one)  
    
    print("finished")
