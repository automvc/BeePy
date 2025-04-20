from bee.config import HoneyConfig

import MyConfig

if __name__ == '__main__':
    
    print("start")
    MyConfig.init()
    print("-----------------")
    config = HoneyConfig() # how to call first time
    # config = HoneyConfig() # how to call first time
    HoneyConfig.cache_max_size
    print(HoneyConfig.cache_max_size)
    print("end")