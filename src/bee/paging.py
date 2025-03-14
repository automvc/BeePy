from bee.config import HoneyConfig
from bee.exception import SqlBeeException
from bee.osql.const import DatabaseConst
from bee.osql.sqlkeyword import K

class Paging:
    
    def to_page_sql(self, sql, start, size):
        config = HoneyConfig()
        dbName = config.get_dbName()
        if dbName is None:
            raise SqlBeeException("dbName is None!")
            # return sql
        elif dbName == DatabaseConst.MYSQL.lower(): 
            return self.__toPageSqlForMySql(sql, start, size)
        elif dbName == DatabaseConst.SQLite.lower(): 
            return self.__toLimitOffsetPaging(sql, start, size)
        else:
            return self.custom_to_page_sql(sql, start, size)  #TODO
        
    def __toPageSqlForMySql(self, sql, start, size): 
        limitStament = " " + K.limit() + " " + str(start) + ", " + str(size)
        sql += limitStament
        return sql
    
    def __toLimitOffsetPaging(self, sql, offset, size): 
        return sql + " " + K.limit() + " " + str(size) + " " + K.offset() + " " + str(offset)
    
    def custom_to_page_sql(self, sql, start, size):
        raise NotImplementedError
           
