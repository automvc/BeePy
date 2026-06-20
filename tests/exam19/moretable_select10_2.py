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

from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

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
    "x": JoinMeta(
        sub_class=S,            # 现在 S 已定义
        joinType=JoinType.WHERE,
        main_fields=["id"],
        sub_fields=["id"],
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
    
    s=S()
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

