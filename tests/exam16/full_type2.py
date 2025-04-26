from bee.config import HoneyConfig

import MyConfig
from bee.honeyfactory import BF
import datetime as dt
from entity.full import Entity

if __name__ == '__main__':
    
    print("start")
    
    MyConfig.init()
    old_naming_translate_type = HoneyConfig.naming_translate_type
    HoneyConfig.naming_translate_type = 3
    
    myTime = dt.time(12, 34, 59)  # dt.time(时、分、秒)
    
    entity = Entity()
    # entity.id = 4
    entity.name = "full-type-test"
    entity.name2 = "name2"
    # entity.flag=False
    entity.flag = True
    entity.price = 3.12
    entity.descstr = "desc"
    entity.remark = "remark"
    entity.modify_date = dt.datetime.today()
    entity.updated_time = myTime  # sqlite不支持time
    entity.created_at = dt.datetime.today()
    
    entity.map = {'name':"John", "age":12}
    print(type(entity.map))
    
    entity.ext = "ext"  # test ext field
    
    # print(entity.modify_date)
    # print(entity.created_at)
    
    # print(entity.__dict__)
    # print(Entity.__dict__)
    # fields = [] 
    # values = []  
    # for name, value in entity.__dict__.items():  
    #     if value is not None:  
    #         fields.append(name)  
    #         values.append(value)
    # print(fields)  
    # print(values)
    
    suidRich = BF.suidRich()
    suidRich.insert(entity)
    
    List = suidRich.select(entity)
    List = suidRich.select(Entity())
    for one in List:
        print(one)
        
    # reset    
    HoneyConfig.naming_translate_type = old_naming_translate_type
    
