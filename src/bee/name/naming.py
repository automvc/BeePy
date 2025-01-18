from bee.name import NameUtil


class UnderScoreAndCamelName:

    @staticmethod
    def toTableName(cls, entityName):
        return NameUtil.toUnderscoreNaming(NameUtil.firstLetterToLowerCase(entityName))
    
    @staticmethod
    def toColumnName(cls, fieldName):
        return NameUtil.toUnderscoreNaming(fieldName)

