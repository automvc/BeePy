class Clazz:
    """ table clazz 's entity """
    id: int = None
    name: str = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)