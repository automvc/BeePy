from bee.condition import ConditionImpl
from bee.osql.bee_enum import Op


if __name__ == '__main__':
    # print(type(None))
    # dbName=None
    # dbName=""
    # if not dbName:
    #     print("not")
    # else:
    #     print("else")
    
    for _ in range(1, 0):
        print("range(1, 0)")
    else:
        print("other")
        
    
    
    condtion = ConditionImpl()
    # condtion.op("name", Op.LIKE_LEFT, "bee")
    # condtion.op("name", Op.LIKE_RIGHT, "bee")
    # condtion.op("name", Op.LIKE_LEFT_RIGHT, "bee")
    # condtion.op("name", Op.LIKE, "bee")
    
    # condtion.op("name", Op.le, "bee")
    # condtion.op("name", Op.ge, "bee")
    # condtion.op("name", Op.eq, "bee")
    
    
    # condtion.op("name", Op.IN, [1,2])
    # condtion.op("name", Op.IN, {1,2})
    condtion.op("name", Op.IN, (1,2) )
    # condtion.op("name", Op.IN, {"1","2"})
    
    # condtion.op("name", Op.IN, "3,4,5")
    
    conditionStruct=condtion.parseCondition()
    
    
    print(conditionStruct.where)
    print(conditionStruct.pv)