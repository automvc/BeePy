import threading

from bee.context import HoneyContext
from bee.factory import BeeFactory
from bee.name.naming import NameTranslate
from bee.osql.const import KeyWork, DatabaseConst

from bee.name.bloom import BloomFilter


class NamingHandler:

    __class_init = False
    __lock = threading.Lock()  # 用于线程安全
    __bf = None

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
        }

    @classmethod
    def __init0(cls):
        if not cls.__class_init:
            with cls.__lock:
                if not cls.__class_init:

                    cls.__bf = BloomFilter(expected_size = 1000, false_positive_rate = 0.001, hash_count = 3)
                    # 添加元素
                    for item in KeyWork.key_work:
                        cls.__bf.add(item)

                    current_db_key_word = NamingHandler.__db_key_word_dict.get(HoneyContext.get_dbname(), "")
                    if current_db_key_word:
                        for item in current_db_key_word:
                            cls.__bf.add(item)

                    # print(len(__bf))

                    cls.__class_init = True

    @staticmethod
    def __is_contain_key_word(name):
        return NamingHandler.__bf.contains(name)

    @staticmethod
    def __is_key_word(name):

        if not name:
            return
        try:
            NamingHandler.__init0()
            f = NamingHandler.__is_contain_key_word(name)
            if f is False:
                return f
        # except Exception as e:
        #     print(e)
        except Exception:
            pass

        return name.lower() in KeyWork.key_work or name.lower() in NamingHandler.__db_key_word_dict.get(HoneyContext.get_dbname(), "")

    @staticmethod
    def getNameTranslate() -> NameTranslate:
        # todo 下一步，要支持使用实时命名规则
        factory = BeeFactory()
        return factory.getInitNameTranslate()

    @staticmethod
    def toTableName(entityName) -> str:
        name = NamingHandler.getNameTranslate().toTableName(entityName)
        return NamingHandler.transform_name_if_keyword(name)

    @staticmethod
    def toColumnName(fieldName) -> str:
        name = NamingHandler.getNameTranslate().toColumnName(fieldName)
        # if name and name.lower() in KeyWork.key_work:
        return NamingHandler.transform_name_if_keyword(name)

    @staticmethod
    def toEntityName(tableName) -> str:
        return NamingHandler.getNameTranslate().toEntityName(tableName)

    @staticmethod
    def toFieldName(columnName) -> str:
        return NamingHandler.getNameTranslate().toFieldName(columnName)

    @staticmethod
    def transform_name_if_keyword(name):
        if not NamingHandler.__is_key_word(name):
            return name

        # warn_keyword(name)

        db_name = HoneyContext.get_dbname()
        if db_name.lower() in [DatabaseConst.MYSQL.lower(), DatabaseConst.MariaDB.lower()]:
            return f"`{name}`"
        elif db_name.lower() == DatabaseConst.MsAccess.lower():
            return f"[{name}]"
        else:
            return f'"{name}"'
