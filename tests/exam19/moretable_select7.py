from typing import List

from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.osql.gen import GenBean
from bee.anno import JoinTable

import MyConfig

# test One to Many

class Hobby:
    """ table hobby 's entity """
    id: int = None
    name: str = None
    category: str = None
    remark: str = None
    stu_no: int = None

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
    
    # hobby=None
    #
    # __joins__ = {
    #     "hobby": JoinTable(
    #         sub_class = Hobby,
    #         joinType = JoinType.JOIN,
    #         main_fields = ["id"],
    #         sub_fields = ["stu_no"],
    #     )
    # }

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
    clazz_place_id: int = None
    
    # student_list =None
    # student_list:List =None
    student_list:list =None 
    clazz_place = None

    def __repr__(self):
        return str(self.__dict__)
    
    __joins__ = {
        # List first
        "student_list": JoinTable(
            sub_class = Student,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["clazz_no"],
            # is_list=True,
        ),
          "clazz_place": JoinTable(
            sub_class = Clazz_place,
            joinType = JoinType.JOIN,
            main_fields = ["clazz_place_id"],
            sub_fields = ["id"],
        )
        
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
    # gen.gen_and_write_bean("clazz_place", path)
    
    clazz = Clazz()
    clazz.name = 'Class1'

    moreTable = BF.moreTable()
    teaList = moreTable.select(clazz)
    
    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

 
