from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.anno import JoinTable

import MyConfig

# one to many, layer is 4.
# 一对多，4层表
class Village:
    """ table village 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    town_id: int = None

    def __repr__(self):
        return str(self.__dict__)


class Town:
    """ table town 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    city_id: int = None

    village_list = None

    __joins__ = {
        "village_list": JoinTable(
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

    town_list = None

    __joins__ = {
        "town_list": JoinTable(
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
        "city_list": JoinTable(
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
    # mylist = moreTable.select_paging(province, 0, 1)
    mylist = moreTable.select_paging(province, 0, 1,"province.name")

    print(len(mylist))

    if mylist:
        for one in mylist:
            print(one)

