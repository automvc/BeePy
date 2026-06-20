from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

import MyConfig

# many to one, layer is 2.
# 多对1
# 2层表
class Province:
    """ table province 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)


class City:
    """ table city 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    province_id: int = None

    province:Province = None

    __joins__ = {
        "province": JoinMeta(
            sub_class = Province,
            joinType = JoinType.JOIN,
            main_fields = ["province_id"],
            sub_fields = ["id"],
        )
    }

    def __repr__(self):
        return str(self.__dict__)

if __name__ == '__main__':
    print("start")

    MyConfig.init()

    city = City()
    moreTable = BF.moreTable()
    teaList = moreTable.select(city)  # 查城市信息，每个城市关联它的省份

    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

