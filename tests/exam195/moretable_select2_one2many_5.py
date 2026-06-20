from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

import MyConfig

# one to many, layer is 5.
# 一对多，5层表
# 不使用is_list = True. 而是在属性用list类型,如：road_list:list=None


class Road:
    """ table road 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    village_id: int = None

    def __repr__(self):
        return str(self.__dict__)


class Village:
    """ table village 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    town_id: int = None

    road_list:list = None

    __joins__ = {
        "road_list": JoinMeta(
            sub_class = Road,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["village_id"],
            # is_list = True
        )
    }

    def __repr__(self):
        return str(self.__dict__)


class Town:
    """ table town 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    city_id: int = None

    village_list:list = None

    __joins__ = {
        "village_list": JoinMeta(
            sub_class = Village,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["town_id"],
            is_list = True
        )
    }

    def __repr__(self):
        return str(self.__dict__)


class City:
    """ table city 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    province_id: int = None

    town_list:list = None

    __joins__ = {
        "town_list": JoinMeta(
            sub_class = Town,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["city_id"],
            # is_list = True
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

    city_list:list = None

    __joins__ = {
        "city_list": JoinMeta(
            sub_class = City,
            joinType = JoinType.JOIN,
            main_fields = ["id"],
            sub_fields = ["province_id"],
            # is_list = True
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

