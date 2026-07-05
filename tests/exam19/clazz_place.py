class Clazz_place:
    """ table clazz_place 's entity """
    id: int = None
    name: str = None
    place: str = None
    year: int = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)