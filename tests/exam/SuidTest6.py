from bee.api import Suid

import MyConfig
from entity.Orders6 import Orders6


# from org.teasoft.exam.entity.Orders6 import Orders6
if __name__ == '__main__':
    print("start")
    MyConfig.init()
    orders = Orders6(**{'name':'bee', 'remark':'test'})  
    print(orders.__dict__)
    print(vars(orders))
    
    suid = Suid()
    orderList = suid.select(orders)
    if orderList is not None:
        for one in orderList: 
            print(one)
    
    print("finished")
