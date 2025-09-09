from datetime import datetime

class Test_name:
    """ table test_name 's entity """
    id: int = None
    my_name: str = None
    name2: str = None
    my_price: float = None
    created_at: datetime
    updated_time: str = None
    flag: bool = None
    set0: str = None
    map: str = None
    list0: str = None
    list1: str = None
    remark: str = None
    tuple0: str = None
    descstr: str = None
    modify_date: datetime
    updated_at2: datetime
    set1: str = None
    map1: str = None
    tuple1: str = None
    set_two: str = None
    map_two: str = None
    tuple_two: str = None
    list_two: str = None
    ttt: str = None

    def __repr__(self):
        return str(self.__dict__)