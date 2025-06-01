

class Custom:

    @staticmethod 
    def custom_pk_statement():
        '''
        return custom primary key statement.
        '''
        return "int(11)"
        # raise NotImplementedError
    
    @staticmethod
    def custom_to_page_sql(sql, start, size):
        '''
        add paging part for sql,if do not want to use framework implement.
        :param sql: SQL select statement which use placeholder.
        :param start: start index,min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: fetch result size (>0).
        '''
        raise NotImplementedError
    
    @staticmethod
    def custom_get_fetch_bean_sql(dbname):
        '''
        define get fetch bean sql by custom.
        :param dbname:
        '''
        raise NotImplementedError
