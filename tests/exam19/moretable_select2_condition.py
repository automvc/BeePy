from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

import MyConfig


class Teacher:
    classno = None
    term = None
    subjectno = None
    teacherno = None
    remark3 = None

    def __repr__(self):
        return  str(self.__dict__)


class Assigncourse:
    __pk__ = "teacherno"
    teacherno = None
    classno = None
    term = None
    subjectno = None
    examno = None
    remark2 = None

    def __repr__(self):
        return  str(self.__dict__)


class Assignexam:

    name = None
    classno = None
    term = None
    subjectno = None
    examno = None
    status = None
    teacherno = None
    remark1 = None

    # 子表对象  TODO 1: 子表对象不能转到select子句
    assigncourse = None
    teacher = None

    def __repr__(self):
        return  str(self.__dict__)

    __joins__ = {
        "assigncourse": JoinMeta(
            sub_class = Assigncourse,
            joinType = JoinType.JOIN,
            main_fields = ["classno", "term", "subjectno"],
            sub_fields = ["classno", "term", "subjectno"],
        ),
        "teacher": JoinMeta(
            sub_class = Teacher,
            joinType = JoinType.LEFT_JOIN,
            main_fields = ["teacherno"],
            sub_fields = ["teacherno"],
        ),
    }


if __name__ == '__main__':
    print("start")

    MyConfig.init()

    # suidRich = SuidRich()
    # suidRich.create_table(Assignexam, True)
    # suidRich.create_table(Teacher, True)
    # suidRich.create_table(Assigncourse, True)

    assignexam = Assignexam()
    assignexam.name = 'Test'
    assignexam.remark1 = 'r1'

    condtion = BF.condition()
    condtion.between('status', 1, 3)

    moreTable = BF.moreTable()
    teaList = moreTable.select(assignexam, condtion)

    # test can use cache
    teaList = moreTable.select(assignexam, condtion)

    suidRich = BF.suidRich()
    assigncourse = Assigncourse()
    assigncourse.teacherno = 1
    assigncourse.remark2 = "new remark2-"
    suidRich.update(assigncourse)

    # test will delete cache after update
    teaList = moreTable.select(assignexam, condtion)

    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

