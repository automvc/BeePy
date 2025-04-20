

class Custom:

    @staticmethod 
    def custom_pk_statement():
        return "int(11)"
        # raise NotImplementedError
    
    @staticmethod
    def custom_to_page_sql(sql, start, size):
        raise NotImplementedError
    
    @staticmethod
    def custom_get_fetch_bean_sql(dbname):
        raise NotImplementedError
