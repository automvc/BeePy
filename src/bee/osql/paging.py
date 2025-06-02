from bee.config import HoneyConfig
from bee.exception import SqlBeeException
from bee.osql.const import DatabaseConst
from bee.osql.sqlkeyword import K

from bee.custom import Custom


class Paging:
    
    def to_page_sql(self, sql, start, size):
        '''
        add paging part for sql.
        :param sql: SQL select statement which use placeholder.
        :param start: start index,min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: fetch result size (>0).
        '''
        dbName = HoneyConfig().get_dbname()
        if not dbName:
            raise SqlBeeException("dbName is None!")
            # return sql
        elif dbName == DatabaseConst.MYSQL.lower(): 
            return self.__toPageSqlForMySql(sql, start, size)
        # elif dbName == DatabaseConst.SQLite.lower(): 
        elif self.__isLimitOffsetDB(dbName):  # v1.6.2
            return self.__toLimitOffsetPaging(sql, start, size)
        else:
            return Custom.custom_to_page_sql(sql, start, size)  # todo
        
    def __toPageSqlForMySql(self, sql, start, size): 
        limitStament = " " + K.limit() + " " + str(start) + ", " + str(size)
        sql += limitStament
        return sql
    
    def __toLimitOffsetPaging(self, sql, offset, size): 
        return sql + " " + K.limit() + " " + str(size) + " " + K.offset() + " " + str(offset)
    
    def __isLimitOffsetDB(self, dbName): 
        return dbName == DatabaseConst.SQLite.lower() or dbName == DatabaseConst.H2.lower() or dbName == DatabaseConst.PostgreSQL.lower() or dbName == DatabaseConst.MsAccess.lower()
    
