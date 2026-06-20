class Hobby:
    """ table hobby 's entity """
    id: int = None
    name: str = None
    category: str = None
    remark: str = None
    stu_no: int = None

    def __repr__(self):
        return str(self.__dict__)