import MyConfig
from bee.honeyfactory import BF
from entity.Student2 import Student2

#update set case 8:
# condition=None
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    suidRich = BF.suidRich()
    
    #entity中，非空的属性，声明在whereFields会转到where中，其它非空的属性转在update set
    stu=Student2()
    stu.age=10
    stu.addr="use new addr"
    
    # condition = BF.condition()
    # #condition中过滤条件都会转在where
    # condition.op("remark", Op.eq, "")
    #
    # #使用condition中set开头的方法，都会用在update set
    # condition.set("addr", "use new addr-update")  # update set
    # condition.set("age", 12)
    #
    # 
    # orderList = suidRich.select(stu,condition)
    # for one in orderList: 
    #     print(one) 
    
    condition=None
    
    # updateNum = suidRich.updateBy(stu,condition,"age")
    updateNum = suidRich.updateBy(stu,condition,"age","name")
    print(updateNum)
# [INFO]  [Bee] sql>>> updateBy SQL: update student2 set addr = ?,age = ? where age = ? and addr = ? and remark = ?
# [INFO]  [Bee] sql>>> params: ['use new addr-update', 12, 10, 'use new addr', '']
    
    orderList = suidRich.select(stu)
    for one in orderList:
        print(one)    
    
    print("finished")
