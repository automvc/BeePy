from bee.api import SuidRich

import MyConfig
from entity.Orders_2025 import Orders_2025


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    suidRich = SuidRich()
    # suidRich.create_table(Orders_2025)
    
    # one = suidRich.select(Orders_2025)
    # print(one)
    
    
