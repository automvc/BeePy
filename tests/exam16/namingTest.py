import MyConfig
from bee.honeyfactory import BF
from bee.osql.bee_enum import Op
import datetime as dt
from entity.naming import TestName


# from entity.full import Entity
#批量插入
if __name__ == '__main__':
    
    print("start")
    
    MyConfig.init()
    
    suidRich=BF.suidRich()
    
    suidRich.create_table(TestName, True)
    
    
    myTime = dt.time(12,34,59)#dt.time(时、分、秒)
    
    entity=TestName()
    entity.id=1
    entity.myName="full-type-test"
    entity.name2="name2"
    # entity.flag=False
    entity.flag=True
    entity.myPrice=3.12
    entity.descstr="desc"
    entity.remark="remark"
    entity.modifyDate=dt.datetime.today()
    entity.updatedTime=myTime #sqlite不支持time
    entity.createdAt=dt.datetime.today()
    entity.ext="ext" #test ext field
    
    entity.map={'name':"John","age":12}
    entity.list0=[1, 2, 3,'a', 4, 5 ]
    entity.tuple0=(1, 2, 3,'b', 4, '5')
    entity.set0=""
    
    entity.map1={'name':"John","age":12}
    entity.list1=[1, 2, 3,'a', 4, 5 ]
    entity.tuple1=(1, 2, 3,'b', 4, '5')
    entity.set1={1, 2, 'c', 4, 3, '5'}
    
    entity.mapTwo={'name':"John","age":12}
    entity.listTwo=[1, 2, 3,'a', 4, 5 ]
    entity.tupleTwo=(1, 2, 3,'b', 4, '5')
    entity.setTwo={1, 2, 'c', 4, 3, '5'}
    
    entity2=TestName()
    entity2.id=2
    entity2.myName="full-type-test2"
    entity2.name2="name2"
    # entity2.flag=False
    entity2.flag=True
    entity2.myPrice=3.12
    entity2.descstr="desc"
    entity2.remark="remark"
    entity2.modifyDate=dt.datetime.today()
    entity2.updatedTime=myTime #sqlite不支持time
    entity2.createdAt=dt.datetime.today()
    entity2.ext="ext" #test ext field
    
    
    # suidRich=BF.suidRich()
    entity_list=[]
    entity_list.append(entity)
    entity_list.append(entity2)
    suidRich.insert_batch(entity_list)
    
    List = suidRich.select(TestName())
    for one in List:
        print(one)
    
    condition = BF.condition()
    condition.op("myName", Op.eq, "full-type-test")
    List = suidRich.select(TestName(), condition)
    for one in List:
        print(one)
    
    # condition = BF.condition()    
    # condition.set("myPrice", 10)
    condition.setAdd("myPrice", 2)   
    u=suidRich.updateBy(TestName(), condition) 
    print(u)   
        
    List = suidRich.select(TestName())
    for one in List:
        print(one)
    
