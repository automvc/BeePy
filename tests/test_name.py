from datetime import datetime, time

class TestName:
    """ table test_name 's entity """
    id: int = None
    myName: str = None
    name2: str = None
    myPrice: float = None
    createdAt: datetime
    updatedTime: time
    flag: bool = None
    set0: str = None
    map: str = None
    list0: str = None
    list1: str = None
    remark: str = None
    tuple0: str = None
    descstr: str = None
    modifyDate: datetime
    updatedAt2: datetime
    set1: str = None
    map1: str = None
    tuple1: str = None
    setTwo: str = None
    mapTwo: str = None
    tupleTwo: str = None
    listTwo: str = None
    ttt: bytes = None

    def __repr__(self):
        return str(self.__dict__)