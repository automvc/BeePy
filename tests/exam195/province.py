class Province:
    """ table province 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)