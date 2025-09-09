from bee.osql.condition_impl import ConditionImpl
from bee.bee_enum import OrderType, FunctionType


if __name__ == '__main__':
    
    for _ in range(1, 0):
        print("range(1, 0)")
    else:
        print("other")
        
    
    
    condtion = ConditionImpl()
    condtion.groupBy("abc")
    condtion.orderBy("abc")
    condtion.orderBy2("abc2",OrderType.DESC)
    condtion.orderBy3(FunctionType.MAX, "total", OrderType.DESC) #-->order by max(total) desc
    
    
    
    conditionStruct=condtion.parseCondition()
    
    
    print(conditionStruct.where)
    print(conditionStruct.pv)