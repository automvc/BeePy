from bee.api import Suid
from test.entity.Student import Student2


if __name__ == '__main__':
    print("start")
    
    # orders=Orders(id=1, name="bee")
    orders=Student2()
    # orders = Test()
    # orders.id=1
    # orders.name = "bee"
    
    suid = Suid()
    orderList = suid.select(orders) #test 
    orderList = suid.select(orders)
    # print(orderList)
    
    for one in orderList: 
        print(one)  
    
    print("finished")
