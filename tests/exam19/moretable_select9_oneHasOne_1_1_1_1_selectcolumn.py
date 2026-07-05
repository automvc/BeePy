from bee.api import SuidRich
from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.osql.gen import GenBean

import MyConfig
from bee.anno import JoinTable


#support join 4 layer.
# --clazz
#     --Student
#        --Hobby
#            --Sub_hobby
#
class Sub_hobby:
    """ table hobby 's entity """
    id: int = None
    name: str = None
    remark: str = None
    main_hobby_id:int = None
    
    def __repr__(self): #要打印，别忘记了
        return str(self.__dict__)
    
    
class Hobby:
    """ table hobby 's entity """
    id: int = None
    name: str = None
    category: str = None
    remark: str = None
    stu_no: int = None
    
    sub_hobby = None
    
    __joins__ = {
        "sub_hobby": JoinTable(
            sub_class = Sub_hobby,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["main_hobby_id"],
        )
    }

    def __repr__(self):
        return str(self.__dict__)
    
class Student:
    """ table student 's entity """
    id: int = None
    name: str = None
    age: int = None
    sex: str = None
    remark: str = None
    clazz_no: int = None
    
    hobby=None
    
    __joins__ = {
        "hobby": JoinTable(
            sub_class = Hobby,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["stu_no"],
        )
    }

    def __repr__(self):
        return str(self.__dict__) 
    
class Clazz_place:
    """ table clazz_place 's entity """
    id: int = None
    name: str = None
    place: str = None
    year: int = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)

class Clazz:
    """ table clazz 's entity """
    id: int = None
    name: str = None
    remark: str = None
    
    student =None 
    # clazz_place = None

    def __repr__(self):
        return str(self.__dict__)
    
    __joins__ = {
        "student": JoinTable(
            sub_class = Student,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["clazz_no"],
        )
        # ,
        #   "clazz_place": JoinTable(
        #     sub_class = Clazz_place,
        #     joinType = JoinType.JOIN,
        #     main_fields = ["clazz_place_id"],
        #     sub_fields = ["id"],
        # )
    }
    

if __name__ == '__main__':
    print("start")

    MyConfig.init()

    # assist =Assist()
    # assist.get_bean_code("clazz")
    
    gen = GenBean()
    # code=gen.get_bean_code("clazz") 
    # print(code)
    
    path="E:\\JavaWeb\\workspace2026-2\\BeePy-automvc\\tests\\exam19"
    
    # gen.gen_and_write_bean("clazz", path)
    # gen.gen_and_write_bean("student", path)
    # gen.gen_and_write_bean("hobby", path)
    
    # suidRich = SuidRich()
    # suidRich.create_table(Hobby, True)
    # suidRich.create_table(Student, True)
    # suidRich.create_table(Sub_hobby, True)
    # suidRich.create_table(Clazz, True)
    # suidRich.create_table(Clazz_place, True)
    
    clazz = Clazz()
    clazz.name = 'Class1'
    
#     hobby.id
# hobby.name

    condition = BF.condition()
    # condition.selectField("clazz.id", "clazz.name")
    # condition.selectField("student.id", "student.name")
    # condition.selectField("clazz.id","student.id", "student.name") #ok
    # condition.selectField("hobby.id", "hobby.name") #layer 3
    # condition.selectField("sub_hobby.id", "sub_hobby.name") #layer 4
    condition.selectField("clazz.id","student.id","sub_hobby.id", "sub_hobby.name") # 中间断层，则前面的可以显示。
    # condition.selectField("clazz.id","student.id","hobby.id","sub_hobby.id", "sub_hobby.name") #有id串联，则所有的都可以显示。

    moreTable = BF.moreTable()
    teaList = moreTable.select(clazz, condition)
    
    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

 
