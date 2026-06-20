from typing import List, Optional, Any

from bee.exception import ConfigBeeException
from bee.typing import JoinMeta

from bee.osql.util import HoneyUtil


class CacheSuidStruct:
    sql:str  # 不带值的
    tableNames:list[str]
    params = None
    returnType:str  # 返回值类型用于过滤缓存的查询结果,防止同一查询sql的不同类型的结果  但更改的操作可不需要用这个值
    suidType:str  # 操作类型
    entityClass = None

    def __init__(self, sql, params, returnType, entityClass, suidType, tableNames):
        self.sql = sql
        self.params = params
        self.returnType = returnType
        self.entityClass = entityClass
        self.suidType = suidType
        if isinstance(tableNames, str):
            # self.tableNames = list(tableNames) #['t', 'a', 'b']
            self.tableNames = [tableNames]
        else:
            self.tableNames = tableNames
        # print(self.tableNames)

    def __str__(self):
        return str(self)


class TableMeta:
    col = None
    type = None
    ynNull:bool = None  # 是否允许为空
    ynKey:bool = None  # 是否是主键
    label = None  # 标题,列名注释
    defaultValue = None
    strLen:int = None
    unique:bool = None
    precisions:int = None
    scale:int = None
    # tablecomment = None
    # tablename = None

    def __repr__(self):
        return  str(self.__dict__)


class MoreTableStructOverall:
    # isHasAnySubListEntity
    has_any_sublist_entity = False

    def __init__(self, has_any_sublist_entity):
        self.has_any_sublist_entity = has_any_sublist_entity


class MoreTableStruct:
    '''
    More table struct for join table use in internal.
    <B>since  1.9.0</B><br>
    '''

    joinType = None
    sub_class = None
    main_fields: List[str] = None  # 主表关联的字段
    sub_fields: List[str] = None  # 从表关联的字段
    sub_alias:str = None  # 从表别名
    main_alias:str = None  # 主表别名

    fieldname: str = None
    sub_object: Optional[Any] = None

    # subDulFieldMap:dict = None  # 列名相同字段

    current_is_list:bool = None  # 当前MoreTableStruct所对应的子表是否是List
    has_next_layer:bool = None

    layer:int = 0
    ptree = None
    type_tree = None
    
    overall:MoreTableStructOverall = None  # just the first element have it.

    def __init__(self, join_meta: JoinMeta, fieldname:str, entity, layer:int, ptree, has_next_layer:bool = None, main_alias:str = None, overall:MoreTableStructOverall = None):
        self.__parse_join_meta(join_meta, fieldname, entity, layer, ptree, has_next_layer, main_alias, overall)

    # ========== 核心专属方法：解析JoinMeta ==========
    def __parse_join_meta(self, join_meta: JoinMeta, fieldname:str, entity, layer, ptree, has_next_layer:bool = None, main_alias:str = None, overall:MoreTableStructOverall = None):
        self.sub_class = join_meta.sub_class
        # print(type(self.sub_class))
        self.joinType = join_meta.joinType
        self.main_fields = join_meta.main_fields
        self.sub_fields = join_meta.sub_fields
        self.sub_alias = join_meta.sub_alias
        self.main_alias = join_meta.main_alias

        self.layer = layer
        self.ptree = ptree

        self.current_is_list = False

        self.fieldname = fieldname
        # self.sub_alias = fieldname
        self.sub_object = getattr(entity, fieldname, None)

        if join_meta.is_list:
            self.current_is_list = join_meta.is_list
            if overall:
                overall.has_any_sublist_entity=True
            # 若是空list,改为None
            if not self.sub_object:
                self.sub_object = None

        else:
            sub_fieldtype = HoneyUtil.get_field_type(HoneyUtil.get_type(entity), fieldname)
            # print(sub_fieldtype)
            if sub_fieldtype in (list, List):
            # if sub_fieldtype is list:
                if join_meta.is_list is False:
                    raise ConfigBeeException(f"JoinMeta setting is inconsistent, is_list {join_meta.is_list}, but the attribute type is list or List")
                self.current_is_list = True
                if overall:
                    overall.has_any_sublist_entity=True

        if not join_meta.sub_alias:
            self.sub_alias = HoneyUtil.get_table_name_by_class(join_meta.sub_class)

        if has_next_layer:
            self.has_next_layer = has_next_layer
            if join_meta.main_alias:
                # 有在JoinMeta声明的，就用
                self.main_alias = join_meta.main_alias
            else:
                self.main_alias = main_alias
