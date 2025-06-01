from bee.osql.gen import GenBean


class Assist:
    '''
    API for assisting ORM.
    '''
    
    __genBean = GenBean() 
    
    def gen_bean(self, table_name:str, file_path: str, file_name:str = None):
        '''
        generate bean file via table name.
        :param table_name: table name
        :param file_path: path of bean file
        :param file_name: file name for bean file; default transform according to table_name.
        '''
        return Assist.__genBean.gen_and_write_bean(table_name, file_path, file_name)

    def get_bean_code(self, table_name:str):
        '''
        get bean code via table name.
        :param table_name:table name
        :return: bean code.
        '''
        return Assist.__genBean.get_bean_code(table_name)
