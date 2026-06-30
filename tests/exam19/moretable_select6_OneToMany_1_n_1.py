from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.osql.gen import GenBean
from bee.anno import JoinTable

import MyConfig

## 1:n:1
# test One to Many
# --clazz
#     --Student (list)
#        --Hobby

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

    hobby = None

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


class Clazz:
    """ table clazz 's entity """
    id: int = None
    name: str = None
    remark: str = None

    # student_list =None
    # student_list:List =None
    student_list:list = None

    def __repr__(self):
        return str(self.__dict__)

    __joins__ = {
        "student_list": JoinTable(
            sub_class = Student,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["clazz_no"],
            # is_list=True,
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

    path = "E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam19"

    # gen.gen_and_write_bean("clazz", path)
    # gen.gen_and_write_bean("student", path)
    # gen.gen_and_write_bean("hobby", path)

    clazz = Clazz()
    clazz.name = 'Class1'

    moreTable = BF.moreTable()
    teaList = moreTable.select(clazz)

    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

