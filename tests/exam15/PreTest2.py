from bee.api import PreparedSql

import MyConfig
from entity.Orders import Orders


if __name__=="__main__":
    MyConfig.init()
    
    pre=PreparedSql()
    
    print("-------------------")
    one =pre.select_dict("SELECT * FROM orders WHERE name=#{name} and id=#{id} and name=#{name}", Orders,params_dict ={"name":"bee1","id":4})
    print(one)
    print("-------------------")
    # one =pre.select_dict("SELECT * FROM orders WHERE name=#{name}", Orders,params_dict = {'name': 'bee'},size=2)
    # print(one)
    print("finished")
