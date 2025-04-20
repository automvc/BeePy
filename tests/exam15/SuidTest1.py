from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    orders=Orders()
    orders.name = "bee"
    
    suidRich = SuidRich()
    one = suidRich.select_first(orders) #test 
    
    print(one)
    
    print("finished")
