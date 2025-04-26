from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    MyConfig.init()  
      
    suidRich = SuidRich()
    # suidRich.create_table(Orders)
    
    one = suidRich.select(Orders())
    print(one)
    
    
