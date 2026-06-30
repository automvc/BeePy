from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.osql.gen import GenBean
from bee.anno import JoinTable

import MyConfig

#support join 4 layer.
# --clazz
#     --Student (list)
#        --Hobby
#            --Sub_hobby
#     --Clazz_place
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
    sub_hobby2 = None
    
    __joins__ = {
        "sub_hobby": JoinTable(
            sub_class = Sub_hobby,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["main_hobby_id"],
        ),
        "sub_hobby2": JoinTable(
            sub_class = Sub_hobby,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["main_hobby_id"],
            sub_alias="sub_hobby2"
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
    
    student_list =None 
    # clazz_place = None

    def __repr__(self):
        return str(self.__dict__)
    
    __joins__ = {
        "student_list": JoinTable(
            sub_class = Student,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["clazz_no"],
            is_list=True,
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
    
    path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam19"
    
    # gen.gen_and_write_bean("clazz", path)
    # gen.gen_and_write_bean("student", path)
    # gen.gen_and_write_bean("hobby", path)
    
    clazz = Clazz()
    clazz.name = 'Class1'
    
    # student=Student()
    clazz.student_list=[]

    moreTable = BF.moreTable()
    teaList = moreTable.select(clazz)
    
    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

 
