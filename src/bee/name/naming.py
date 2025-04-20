from bee.config import HoneyConfig
from bee.name import NameUtil


class NameTranslate:

    def toTableName(self, entityName):
        raise NotImplementedError

    def toColumnName(self, fieldName):
        raise NotImplementedError

    def toEntityName(self, tableName):
        raise NotImplementedError

    def toFieldName(self, columnName):
        raise NotImplementedError

"""
 * Python Camel and Databse UnderScore transform.
 * Python<-->DB,eg: orderNo<-->order_no.
 * @author Kingstar
 * @since  1.5
"""


class UnderScoreAndCamelName(NameTranslate):

    def toTableName(self, entityName):
        if not entityName:
            return entityName
        return NameUtil.toUnderscoreNaming(NameUtil.firstLetterToLower(entityName))

    def toColumnName(self, fieldName):
        if not fieldName:
            return fieldName
        return NameUtil.toUnderscoreNaming(fieldName)

    def toEntityName(self, tableName):
        if not tableName:
            return tableName
        naming_to_lower_before = HoneyConfig.naming_to_lower_before
        if naming_to_lower_before:
            tableName = tableName.lower() 
        return NameUtil.firstLetterToUpper(NameUtil.toCamelNaming(tableName))  
    
    def toFieldName(self, columnName):
        if not columnName:
            return columnName
        naming_to_lower_before = HoneyConfig.naming_to_lower_before
        if naming_to_lower_before:
            columnName = columnName.lower()  
        return NameUtil.toCamelNaming(columnName)
    
    
class OriginalName(NameTranslate):

    def toTableName(self, entityName):
        if not entityName:
            return entityName
        return NameUtil.firstLetterToLower(entityName)

    def toColumnName(self, fieldName):
        if not fieldName:
            return fieldName
        return fieldName

    def toEntityName(self, tableName):
        if not tableName:
            return tableName
        return NameUtil.firstLetterToUpper(tableName)

    def toFieldName(self, columnName):
        if not columnName:
            return columnName
        return columnName


class DbUpperAndPythonLower(NameTranslate):

    def toTableName(self, entityName):
        if not entityName:
            return entityName
        return entityName.upper()

    def toColumnName(self, fieldName):
        if not fieldName:
            return fieldName
        return fieldName.upper()

    def toEntityName(self, tableName):
        if not tableName:
            return tableName
        return NameUtil.firstLetterToUpper(tableName.lower())

    def toFieldName(self, columnName):
        if not columnName:
            return columnName
        return columnName.lower()

"""  
 * Python Camel and Database UnderScore & Upper transform.
 * Python<-->DB,eg: orderNo<-->ORDER_NO.
 * @author Kingstar
 * @since  1.5
"""


class UpperUnderScoreAndCamelName(UnderScoreAndCamelName):

    def toTableName(self, entityName):
        return super.toTableName(entityName).upper()

    def toColumnName(self, fieldName):
        return super.toColumnName(fieldName).upper()
    
    def toEntityName(self, tableName):
        # need lower first if the name has upper 
        tableName = tableName.lower()
        return NameUtil.firstLetterToUpper(NameUtil.toCamelNaming(tableName))

    def toFieldName(self, columnName):
        # need lower first if the name has upper 
        columnName = columnName.lower()  # if not , BEE_NAME->BEENAME  -> ??
        return NameUtil.toCamelNaming(columnName)
