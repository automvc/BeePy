from bee.config import HoneyConfig
from bee.osql.const import DatabaseConst


class Paging:
    
    def to_page_sql(self, sql, start, size):
        config = HoneyConfig()
        dbName = config.get_dbName()
        if dbName is None:
            # 使用配置的dbName TODO  抛异常
            return sql
        elif dbName == DatabaseConst.MYSQL.lower(): 
            return self.__toPageSqlForMySql(sql, start, size)
        elif dbName == DatabaseConst.SQLite.lower(): 
            return self.__toLimitOffsetPaging(sql, start, size)
        
    def __toPageSqlForMySql(self, sql, start, size): 
        limitStament = " " + "limit" + " " + str(start) + ", " + str(size)
        sql += limitStament
        return sql
    
    def __toLimitOffsetPaging(self, sql, offset, size): 
        return sql + " " + "limit" + " " + str(size) + " " + "offset" + " " + str(offset)
           
