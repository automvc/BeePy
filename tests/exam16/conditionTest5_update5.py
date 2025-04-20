import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2

#update set case 5:
#entity no value
#use condtion just setXxx; no op for where
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    #entity中，非空的属性，声明在whereFields会转到where中，其它非空的属性转在update set
    stu=Student2()
    
    condition = BF.condition()
    #condition中过滤条件都会转在where
    # condition.op("remark", Op.eq, "")
    
    #使用condition中set开头的方法，都会用在update set
    condition.set("addr", "use new addr")  # update set
    condition.set("age", 12)
    
    suidRich = BF.suidRich()
    orderList = suidRich.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    updateNum = suidRich.updateBy(stu,condition,"age")
    print(updateNum)
# [INFO]  [Bee] sql>>> updateBy SQL: update student2 set addr = ?,age = ? where age is null
# [INFO]  [Bee] sql>>> params: ['use new addr', 12]
    
    orderList = suidRich.select(stu)
    for one in orderList:
        print(one)    
    
    print("finished")
