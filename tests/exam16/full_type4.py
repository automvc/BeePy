import MyConfig
from bee.config import HoneyConfig
from bee.api import SuidRich
import datetime as dt
from entity.full import Entity

# 批量插入
if __name__ == '__main__':
    
    print("start")
    
    MyConfig.init()
    
    old_naming_translate_type = HoneyConfig.naming_translate_type
    HoneyConfig.naming_translate_type = 3
    
    myTime = dt.time(12, 34, 59)  # dt.time(时、分、秒)
    
    entity = Entity()
    # entity.id = 1
    entity.name = "full-type-test"
    entity.name2 = "name2"
    entity.flag = False
    # entity.flag=True
    entity.price = 3.12
    entity.descstr = "desc"
    entity.remark = "remark"
    entity.modify_date = dt.datetime.today()
    entity.updated_time = myTime  # sqlite不支持time
    entity.created_at = dt.datetime.today()
    entity.ext = "ext"  # test ext field
    
    entity.map = {'name':"John", "age":12}
    entity.list0 = [1, 2, 3, 'a', 4, 5 ]
    entity.tuple0 = (1, 2, 3, 'b', 4, '5')
    entity.set0 = ""
    
    entity.map1 = {'name':"John", "age":12}
    entity.list1 = [1, 2, 3, 'a', 4, 5 ]
    entity.tuple1 = (1, 2, 3, 'b', 4, '5')
    entity.set1 = {1, 2, 'c', 4, 3, '5'}
    
    entity2 = Entity()
    # entity2.id = 2
    entity2.name = "full-type-test"
    entity2.name2 = "name2"
    # entity2.flag=False
    entity2.flag = True
    entity2.price = 3.12
    entity2.descstr = "desc"
    entity2.remark = "remark"
    entity2.modify_date = dt.datetime.today()
    entity2.updated_time = myTime  # sqlite不支持time
    entity2.created_at = dt.datetime.today()
    entity2.ext = "ext"  # test ext field

    suidRich = SuidRich()
    entity_list = []
    entity_list.append(entity)
    entity_list.append(entity2)
    suidRich.insert_batch(entity_list)
    
    List = suidRich.select(Entity())
    for one in List:
        print(one)
        
    # reset    
    HoneyConfig.naming_translate_type = old_naming_translate_type
    
    print("--------full_type4---------,HoneyConfig.cache_donot_put_cache_result_min_size  :", HoneyConfig.cache_donot_put_cache_result_min_size)
    print("--------full_type4---------,HoneyConfig.naming_to_lower_before  :", HoneyConfig.naming_to_lower_before)
    print("--------full_type4---------,HoneyConfig.show_sql_spent_time  :", HoneyConfig.show_sql_spent_time)
    
