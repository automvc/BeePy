class Road:
    """ table road 's entity """
    id: int = None
    name: str = None
    level: int = None
    remark: str = None
    village_id: int = None

    def __repr__(self):
        return str(self.__dict__)