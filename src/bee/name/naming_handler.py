from bee.context import HoneyContext
from bee.factory import BeeFactory
from bee.name.naming import NameTranslate
from bee.osql.const import KeyWork, DatabaseConst


class NamingHandler:
    
    __db_key_word_dict = {
        DatabaseConst.MYSQL.lower():KeyWork.mysql_keywords,
        DatabaseConst.ORACLE.lower():KeyWork.oracle_keywords,
        DatabaseConst.MariaDB.lower():KeyWork.mariadb_keywords,
        DatabaseConst.H2.lower():KeyWork.h2_keywords,
        DatabaseConst.SQLite.lower():KeyWork.sqlite_keywords,
        DatabaseConst.PostgreSQL.lower():KeyWork.postgresql_keywords,
        DatabaseConst.MsAccess.lower():KeyWork.msaccess_keywords,
        DatabaseConst.Kingbase.lower():KeyWork.kingbase_keywords,
        DatabaseConst.DM.lower():KeyWork.dm_keywords,
        DatabaseConst.OceanBase.lower():KeyWork.oceanbase_keywords
        }
    
    @staticmethod
    def __is_key_word(name):
        return name.lower() in KeyWork.key_work or name.lower() in NamingHandler.__db_key_word_dict.get(HoneyContext.get_dbname(), "")
    
    @staticmethod
    def getNameTranslate() -> NameTranslate:
        # todo 下一步，要支持使用实时命名规则
        factory = BeeFactory()
        return factory.getInitNameTranslate()
    
    @staticmethod
    def toTableName(entityName) -> str:
        name = NamingHandler.getNameTranslate().toTableName(entityName)
        if name and NamingHandler.__is_key_word(name):
            name = "`" + name + "`";
        return name

    @staticmethod
    def toColumnName(fieldName) -> str:
        name = NamingHandler.getNameTranslate().toColumnName(fieldName)
        # if name and name.lower() in KeyWork.key_work:
        if name and NamingHandler.__is_key_word(name):
            name = "`" + name + "`";
        return name
    
    @staticmethod
    def toEntityName(tableName) -> str:
        return NamingHandler.getNameTranslate().toEntityName(tableName)
    
    @staticmethod
    def toFieldName(columnName) -> str:
        return NamingHandler.getNameTranslate().toFieldName(columnName)

