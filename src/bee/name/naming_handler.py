from bee.factory import BeeFactory
from bee.name.naming import NameTranslate
from bee.osql.const import KeyWork


class NamingHandler:
    
    @staticmethod
    def getNameTranslate() -> NameTranslate:
        # todo 下一步，要支持使用实时命名规则
        factory = BeeFactory()
        return factory.getInitNameTranslate()
    
    @staticmethod
    def toTableName(entityName) -> str:
        return NamingHandler.getNameTranslate().toTableName(entityName)

    @staticmethod
    def toColumnName(fieldName) -> str:
        name = NamingHandler.getNameTranslate().toColumnName(fieldName)
        if name and name.lower() in KeyWork.key_work: # TODO 具体DB还要
            name = "`" + name + "`";
        return name
    
    @staticmethod
    def toEntityName(tableName) -> str:
        return NamingHandler.getNameTranslate().toEntityName(tableName)
    
    @staticmethod
    def toFieldName(columnName) -> str:
        return NamingHandler.getNameTranslate().toFieldName(columnName)
