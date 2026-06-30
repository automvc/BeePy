from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.anno import JoinTable

import MyConfig

# many to one, layer is 5.
# 多对1
# 5层表
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
        "province": JoinTable(
            sub_class = Province,
            joinType = JoinType.JOIN,
            main_fields = ["province_id"],
            sub_fields = ["id"],
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
    city:City = None

    __joins__ = {
        "city": JoinTable(
            sub_class = City,
            joinType = JoinType.JOIN,
            main_fields = ["city_id"],
            sub_fields = ["id"],
        )
    }

    def __repr__(self):
        return str(self.__dict__)


class Village:
    """ table village 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    town_id: int = None

    town:Town = None

    __joins__ = {
        "town": JoinTable(
            sub_class = Town,
            joinType = JoinType.JOIN,
            main_fields = ["town_id"],
            sub_fields = ["id"],
        )
    }

    def __repr__(self):
        return str(self.__dict__)


class Road:
    """ table road 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    village_id: int = None

    village:Village = None

    __joins__ = {
        "village": JoinTable(
            sub_class = Village,
            joinType = JoinType.JOIN,
            main_fields = ["village_id"],
            sub_fields = ["id"],
        )
    }

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    print("start")

    MyConfig.init()

    # city = City()
    # moreTable = BF.moreTable()
    # teaList = moreTable.select(city)  # 查城市信息，每个城市关联它的省份
    # print(len(teaList))
    #
    # if teaList:
    #     for one in teaList:
    #         print(one)
    #
    # town = Town()
    # moreTable = BF.moreTable()
    # teaList = moreTable.select(town)
    #
    # print(len(teaList))
    #
    # if teaList:
    #     for one in teaList:
    #         print(one)

    road = Road()
    moreTable = BF.moreTable()
    teaList = moreTable.select(road)

    print(len(teaList))

    if teaList:
        for one in teaList:
            print(one)

