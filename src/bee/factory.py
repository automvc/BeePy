from bee.config import HoneyConfig
from bee.name.naming import NameTranslate, UnderScoreAndCamelName, \
    UpperUnderScoreAndCamelName, OriginalName, DbUpperAndPythonLower


class BeeFactory:
    """
    Bee Factory.
    """

    __connection = None

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def set_connection(self, connection):
        '''
        set connection
        '''
        BeeFactory.__connection = connection

    def get_connection(self):
        '''
        get connection
        '''
        return BeeFactory.__connection

    def __init__(self):
        self.__nameTranslate = None

    def getInitNameTranslate(self) -> NameTranslate:
        '''
        #     (DB<-->Python),
        # 1: order_no<-->orderNo
        # 2: ORDER_NO<-->orderNo
        # 3: original,
        # 4: ORDER_NO<-->order_no (DbUpperAndPythonLower)
        '''
        if self.__nameTranslate is None:
            translateType = HoneyConfig.naming_translate_type
            if translateType == 1:
                self.__nameTranslate = UnderScoreAndCamelName()
            elif translateType == 2:
                self.__nameTranslate = UpperUnderScoreAndCamelName()
            elif translateType == 3:
                self.__nameTranslate = OriginalName()
            elif translateType == 4:
                self.__nameTranslate = DbUpperAndPythonLower()
            # else:__nameTranslate = UnderScoreAndCamelName()
            else:
                self.__nameTranslate = OriginalName()  # v1.6.2

        return self.__nameTranslate
