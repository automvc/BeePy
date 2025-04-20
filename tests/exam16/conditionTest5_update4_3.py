import MyConfig
from bee.honeyfactory import BF
from entity.Student3 import Student3

#update set case 4:
#entity have value
#use condtion where between and setXxx
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    suidRich = BF.suidRich()
    # suidRich.create_table(Student3, True)
    
    #entity中，非空的属性，声明在whereFields会转到where中，其它非空的属性转在update set
    stu=Student3()
    stu.addr=""
    
    condition = BF.condition()
    #condition中过滤条件都会转在where
    # condition.op("remark", Op.eq, "")
    condition.between("age", 20, 21)
    
    #使用condition中set开头的方法，都会用在update set
    condition.set("addr", "use new addr-update2")  # update set
    # condition.set("remark", None)  # update set remark=null
    
    
    orderList = suidRich.select(stu,condition)
    for one in orderList: 
        print(one) 
    
    updateNum = suidRich.updateBy(stu,condition,"remark")
    print(updateNum)
# [INFO]  [Bee] sql>>> updateBy SQL: update student3 set addr = %s , addr = %s where remark is null and age between %s and %s
# [INFO]  [Bee] sql>>> params: ['', 'use new addr-update2', 20, 21]
    
    orderList = suidRich.select(stu)
    for one in orderList:
        print(one)    
    
    print("finished")
