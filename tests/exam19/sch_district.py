class Sch_district:
    """ table sch_district 's entity """
    id: int = None
    district_name: str = None
    remark: str = None

    def __repr__(self):
        return str(self.__dict__)