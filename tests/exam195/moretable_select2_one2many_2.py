from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

import MyConfig

# one to many, layer is 3.
# 一对多，3层表


class Town:
    """ table town 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    city_id: int = None

    # village_list:Village = None

    # __joins__ = {
    #     "village_list": JoinMeta(
    #         sub_class = Village,
    #         joinType = JoinType.JOIN,
    #         main_fields = ["id"],
    #         sub_fields = ["town_id"],
    #     )
    # }

    def __repr__(self):
        return str(self.__dict__)


class City:
    """ table city 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    province_id: int = None

    town_list = None

    __joins__ = {
        "town_list": JoinMeta(
            sub_class = Town,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["city_id"],
            is_list = True
        )
    }

    def __repr__(self):
        return str(self.__dict__)


class Province:
    """ table province 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None

    city_list = None

    __joins__ = {
        "city_list": JoinMeta(
            sub_class = City,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["province_id"],
            is_list = True
        )
    }

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    print("start")

    MyConfig.init()

    province = Province()
    moreTable = BF.moreTable()
    teaList = moreTable.select(province)

    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

