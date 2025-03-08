from bee.name.naming import NameTranslate, UnderScoreAndCamelName, \
    UpperUnderScoreAndCamelName, OriginalName, DbUpperAndJavaLower


class HoneyFactory:
    
    __nameTranslate = None
    
    def getInitNameTranslate(self) -> NameTranslate:
        
        if self.__nameTranslate is None:
            # int translateType=HoneyConfig.getHoneyConfig().naming_translateType;
            translateType = 1  # TODO from config
            if translateType == 1: __nameTranslate = UnderScoreAndCamelName()
            elif translateType == 2: __nameTranslate = UpperUnderScoreAndCamelName()
            elif translateType == 3: __nameTranslate = OriginalName()
            elif translateType == 4: __nameTranslate = DbUpperAndJavaLower()
            else:__nameTranslate = UnderScoreAndCamelName()
                
        return __nameTranslate;
