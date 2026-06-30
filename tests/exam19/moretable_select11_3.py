from __future__ import annotations

from bee.api import SuidRich
from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.osql.gen import GenBean
from bee.anno import JoinTable

import MyConfig


class A:
    id: int = None
    sname: str = None
   
    sno: int = None
    age: int = None
    
    y: "B" = None
    __joins__ = {}
    def __repr__(self): return str(self.__dict__)

class B:
    id: int = None
    sname: str = None
    sno: int = None
    age: int = None
    
    x: A = None
    __joins__ = {}
    def __repr__(self): return str(self.__dict__)

# 假设 JoinTable, JoinType 已定义在此之前
A.__joins__ = {
    "y": JoinTable(
        sub_class=B,
        joinType=JoinType.JOIN,
        main_fields=["id"],
        sub_fields=["id"],
        sub_alias='y',
        main_alias="x"
    )
}

B.__joins__ = { #select子句，要通过__joins__ {}的key，排除不要查的字段。 不写会有多余的字段。
    "x": JoinTable(
        sub_class=A,
        joinType=JoinType.JOIN,
        main_fields=["id"],
        sub_fields=["id"],
        sub_alias='x',
    )
}


if __name__ == '__main__':
    print("start")

    MyConfig.init()

    # assist =Assist()
    # assist.get_bean_code("clazz")
    
    # gen = GenBean()
    # code=gen.get_bean_code("s") 
    # print(code)
    
    s=A()
    s.sname="WANG"

    moreTable = BF.moreTable()
    teaList = moreTable.select(s)
    
    # test can use cache
    teaList = moreTable.select(s)
    
    # suidRich = BF.suidRich()
    # assigncourse = Assigncourse()
    # assigncourse.teacherno = 1
    # assigncourse.remark2 = "new remark2"
    # suidRich.update(assigncourse)
    
    # test will delete cache after update
    teaList = moreTable.select(s)
    print(len(teaList))
    
    if teaList:
        for one in teaList:
            print(one)

