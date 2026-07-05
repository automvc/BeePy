class Student:
    """ table student 's entity """
    id: int = None
    name: str = None
    age: int = None
    sex: str = None
    remark: str = None
    clazz_no: int = None

    def __repr__(self):
        return str(self.__dict__)