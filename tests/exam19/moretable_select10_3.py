"""
Test s x, s y case.

SELECT
    x.id,
    x.sname,
    x.sno,
    x.age,
    y.id 'y.id',
    y.sname 'y.sname',
    y.sno 'y.sno',
    y.age 'y.age' 
FROM
    s x,
    s y 
WHERE
    x.id = y.id 
    AND x.sname = 'WANG'
"""

from __future__ import annotations

from operator import gt

from bee.bee_enum import JoinType, Op
from bee.honeyfactory import BF
from bee.anno import JoinTable

import MyConfig


class S:
    """ table s 's entity """
    id: int = None
    sname: str = None
    sno: int = None
    age: int = None
    
    x:S=None  #Undefined variable: S
    
    __joins__ = {}

    def __repr__(self):
        return str(self.__dict__)

S.__joins__ = {
    "x": JoinTable(
        sub_class=S,            # 现在 S 已定义
        joinType=JoinType.WHERE,
        # main_fields=["id"],
        # sub_fields=["id"],
        main_fields=[],
        sub_fields=[],
        sub_alias='y',
        main_alias='x'
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
    
    # y.sname = 'WANG'
    # and x.sno>y.sno
    # and x.age<y.age
    
    s=S()
    # s.sname="WANG"
    condition=BF.condition()
    condition.op("y.sname",Op.eq,"WANG");
    condition.opWithField("x.sno", Op.gt, "y.sno")
    condition.opWithField("x.age", Op.lt, "y.age")
    
    condition.selectField("x.sname")

    moreTable = BF.moreTable()
    teaList = moreTable.select(s,condition)
    
    # test can use cache
    teaList = moreTable.select(s,condition)
    
    
    print(len(teaList))
    
    if teaList:
        for one in teaList:
            print(one)

