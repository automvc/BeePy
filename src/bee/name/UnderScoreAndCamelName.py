from bee.name import NameUtil


def toTableName(entityName):
    return NameUtil.toUnderscoreNaming(NameUtil.firstLetterToLowerCase(entityName))


def toColumnName(fieldName):
    return NameUtil.toUnderscoreNaming(fieldName)


# def toEntityName(tableName):
#         if (HoneyConfig.getHoneyConfig().naming_toLowerCaseBefore):
#             # need lowercase first if the name has upper case
#             tableName = tableName.toLowerCase()
#         return NameUtil.firstLetterToUpperCase(NameUtil.toCamelNaming(tableName))
#
#
# def toFieldName(columnName):
#         if (HoneyConfig.getHoneyConfig().naming_toLowerCaseBefore) :
#             # need lowercase first if the name has upper case
#             columnName = columnName.toLowerCase(); # if not , BEE_NAME -> BEENAME -> ??
#         return NameUtil.toCamelNaming(columnName)
