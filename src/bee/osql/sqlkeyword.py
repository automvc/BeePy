from bee.util import HoneyUtil

class SqlKeyWord:  
    def select(self):  
        raise NotImplementedError  

    def as_(self):  
        raise NotImplementedError  

    def from_(self):  
        raise NotImplementedError  

    def where(self):  
        raise NotImplementedError  

    def insert(self):  
        raise NotImplementedError  

    def replace(self):  
        raise NotImplementedError  

    def into(self):  
        raise NotImplementedError  

    def values(self):  
        raise NotImplementedError  

    def and_(self):  
        raise NotImplementedError  

    def or_(self):  
        raise NotImplementedError  

    def not_(self):  
        raise NotImplementedError  

    def null(self):  
        raise NotImplementedError  

    def isnull(self):  
        raise NotImplementedError  

    def is_not_null(self):  
        raise NotImplementedError  

    def update(self):  
        raise NotImplementedError  

    def set(self):  
        raise NotImplementedError  

    def delete(self):  
        raise NotImplementedError  

    def order_by(self):  
        raise NotImplementedError  

    def count(self):  
        raise NotImplementedError  

    def asc(self):  
        raise NotImplementedError  

    def on(self):  
        raise NotImplementedError  

    def limit(self):  
        raise NotImplementedError  

    def offset(self):  
        raise NotImplementedError  

    def top(self):  
        raise NotImplementedError  

    def group_by(self):  
        raise NotImplementedError  

    def having(self):  
        raise NotImplementedError  

    def between(self):  
        raise NotImplementedError  

    def not_between(self):  
        raise NotImplementedError  

    def for_update(self):  
        raise NotImplementedError  

    def distinct(self):  
        raise NotImplementedError  

    def join(self):  
        raise NotImplementedError  

    def inner_join(self):  
        raise NotImplementedError  

    def left_join(self):  
        raise NotImplementedError  

    def right_join(self):  
        raise NotImplementedError  

    def in_(self):  
        raise NotImplementedError  

    def not_in(self):  
        raise NotImplementedError  

    def exists(self):  
        raise NotImplementedError  

    def not_exists(self):  
        raise NotImplementedError  

    def union(self):  
        raise NotImplementedError  

    def union_all(self):  
        raise NotImplementedError  

    def truncate(self):  
        raise NotImplementedError  

    def table(self):  
        raise NotImplementedError  

    def drop(self):  
        raise NotImplementedError  

    def if_(self):  
        raise NotImplementedError  

    def to_date(self):  
        raise NotImplementedError  


class UpperKey(SqlKeyWord):  
    def select(self):  
        return "SELECT"  

    def as_(self):  
        return "AS"  

    def from_(self):  
        return "FROM"  

    def where(self):  
        return "WHERE"  

    def insert(self):  
        return "INSERT"  

    def replace(self):  
        return "REPLACE"  

    def into(self):  
        return "INTO"  

    def values(self):  
        return "VALUES"  

    def and_(self):  
        return "AND"  

    def or_(self):  
        return "OR"  

    def not_(self):  
        # return "NOT"  
        return "!"  

    def null(self):  
        return "NULL"  

    def isnull(self):  
        return "IS NULL"  

    def is_not_null(self):  
        return "IS NOT NULL"  

    def update(self):  
        return "UPDATE"  

    def set(self):  
        return "SET"  

    def delete(self):  
        return "DELETE"  

    def order_by(self):  
        return "ORDER BY"  

    def count(self):  
        return "COUNT"  

    def asc(self):  
        return "ASC"  

    def on(self):  
        return "ON"  

    def limit(self):  
        return "LIMIT"  

    def offset(self):  
        return "OFFSET"  

    def top(self):  
        return "TOP"  

    def group_by(self):  
        return "GROUP BY"  

    def having(self):  
        return "HAVING"  

    def between(self):  
        return "BETWEEN"  

    def not_between(self):  
        return "NOT BETWEEN"  

    def for_update(self):  
        return "FOR UPDATE"  

    def distinct(self):  
        return "DISTINCT"  

    def join(self):  
        return "JOIN"  

    def inner_join(self):  
        return "INNER JOIN"  

    def left_join(self):  
        return "LEFT JOIN"  

    def right_join(self):  
        return "RIGHT JOIN"  

    def in_(self):  
        return "IN"  

    def not_in(self):  
        return "NOT IN"  

    def exists(self):  
        return "EXISTS"  

    def not_exists(self):  
        return "NOT EXISTS"  

    def union(self):  
        return "UNION"  

    def union_all(self):  
        return "UNION ALL"  

    def truncate(self):  
        return "TRUNCATE"  

    def table(self):  
        return "TABLE"  

    def drop(self):  
        return "DROP"  

    def if_(self):  
        return "IF"  

    def to_date(self):  
        return "TO_DATE"  


class LowerKey(SqlKeyWord):  
    def select(self):  
        return "select"  

    def as_(self):  
        return "as"  

    def from_(self):  
        return "from"  

    def where(self):  
        return "where"  

    def insert(self):  
        return "insert"  

    def replace(self):  
        return "replace"  

    def into(self):  
        return "into"  

    def values(self):  
        return "values"  

    def and_(self):  
        return "and"  

    def or_(self):  
        return "or"  

    def not_(self):  
        # return "not"  
        return "!"  

    def null(self):  
        return "null"  

    def isnull(self):  
        return "is null"  

    def is_not_null(self):  
        return "is not null"  

    def update(self):  
        return "update"  

    def set(self):  
        return "set"  

    def delete(self):  
        return "delete"  

    def order_by(self):  
        return "order by"  

    def count(self):  
        return "count"  

    def asc(self):  
        return "asc"  

    def on(self):  
        return "on"  

    def limit(self):  
        return "limit"  

    def offset(self):  
        return "offset"  

    def top(self):  
        return "top"  

    def group_by(self):  
        return "group by"  

    def having(self):  
        return "having"  

    def between(self):  
        return "between"  

    def not_between(self):  
        return "not between"  

    def for_update(self):  
        return "for update"  

    def distinct(self):  
        return "distinct"  

    def join(self):  
        return "join"  

    def inner_join(self):  
        return "inner join"  

    def left_join(self):  
        return "left join"  

    def right_join(self):  
        return "right join"  

    def in_(self):  
        return "in"  

    def not_in(self):  
        return "not in"  

    def exists(self):  
        return "exists"  

    def not_exists(self):  
        return "not exists"  

    def union(self):  
        return "union"  

    def union_all(self):  
        return "union all"  

    def truncate(self):  
        return "truncate"  

    def table(self):  
        return "table"  

    def drop(self):  
        return "drop"  

    def if_(self):  
        return "if"  

    def to_date(self):  
        return "to_date"  


class K:  
    __sql_keywords = None  

    @classmethod  
    def _get_sql_keywords(cls):
        try:  
            if HoneyUtil.is_sql_key_word_upper():  # 根据配置指定是用大写还是小写  
                return UpperKey()
        except Exception:
            pass
        
        return LowerKey()  # 默认使用小写
          

    @classmethod  
    def _initialize(cls):  
        if not cls.__sql_keywords:  
            cls.__sql_keywords = cls._get_sql_keywords()  

    @classmethod  
    def select(cls):  
        cls._initialize()  
        return cls.__sql_keywords.select()  

    @classmethod  
    def as_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.as_()  

    @classmethod  
    def from_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.from_()  

    @classmethod  
    def where(cls):  
        cls._initialize()  
        return cls.__sql_keywords.where()  

    @classmethod  
    def insert(cls):  
        cls._initialize()  
        return cls.__sql_keywords.insert()  

    @classmethod  
    def replace(cls):  
        cls._initialize()  
        return cls.__sql_keywords.replace()  

    @classmethod  
    def into(cls):  
        cls._initialize()  
        return cls.__sql_keywords.into()  

    @classmethod  
    def values(cls):  
        cls._initialize()  
        return cls.__sql_keywords.values()  

    @classmethod  
    def and_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.and_()  

    @classmethod  
    def or_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.or_()  

    @classmethod  
    def not_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.not_()  

    @classmethod  
    def null(cls):  
        cls._initialize()  
        return cls.__sql_keywords.null()  

    @classmethod  
    def isnull(cls):  
        cls._initialize()  
        return cls.__sql_keywords.isnull()  

    @classmethod  
    def is_not_null(cls):  
        cls._initialize()  
        return cls.__sql_keywords.is_not_null()  

    @classmethod  
    def update(cls):  
        cls._initialize()  
        return cls.__sql_keywords.update()  

    @classmethod  
    def set(cls):  
        cls._initialize()  
        return cls.__sql_keywords.set()  

    @classmethod  
    def delete(cls):  
        cls._initialize()  
        return cls.__sql_keywords.delete()  

    @classmethod  
    def order_by(cls):  
        cls._initialize()  
        return cls.__sql_keywords.order_by()  

    @classmethod  
    def count(cls):  
        cls._initialize()  
        return cls.__sql_keywords.count()  

    @classmethod  
    def asc(cls):  
        cls._initialize()  
        return cls.__sql_keywords.asc()  

    @classmethod  
    def on(cls):  
        cls._initialize()  
        return cls.__sql_keywords.on()  

    @classmethod  
    def limit(cls):  
        cls._initialize()  
        return cls.__sql_keywords.limit()  

    @classmethod  
    def offset(cls):  
        cls._initialize()  
        return cls.__sql_keywords.offset()  

    @classmethod  
    def top(cls):  
        cls._initialize()  
        return cls.__sql_keywords.top()  

    @classmethod  
    def group_by(cls):  
        cls._initialize()  
        return cls.__sql_keywords.group_by()  

    @classmethod  
    def having(cls):  
        cls._initialize()  
        return cls.__sql_keywords.having()  

    @classmethod  
    def between(cls):  
        cls._initialize()  
        return cls.__sql_keywords.between()  

    @classmethod  
    def not_between(cls):  
        cls._initialize()  
        return cls.__sql_keywords.not_between()  

    @classmethod  
    def for_update(cls):  
        cls._initialize()  
        return cls.__sql_keywords.for_update()  

    @classmethod  
    def distinct(cls):  
        cls._initialize()  
        return cls.__sql_keywords.distinct()  

    @classmethod  
    def join(cls):  
        cls._initialize()  
        return cls.__sql_keywords.join()  

    @classmethod  
    def inner_join(cls):  
        cls._initialize()  
        return cls.__sql_keywords.inner_join()  

    @classmethod  
    def left_join(cls):  
        cls._initialize()  
        return cls.__sql_keywords.left_join()  

    @classmethod  
    def right_join(cls):  
        cls._initialize()  
        return cls.__sql_keywords.right_join()  

    @classmethod  
    def in_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.in_()  

    @classmethod  
    def not_in(cls):  
        cls._initialize()  
        return cls.__sql_keywords.not_in()  

    @classmethod  
    def exists(cls):  
        cls._initialize()  
        return cls.__sql_keywords.exists()  

    @classmethod  
    def not_exists(cls):  
        cls._initialize()  
        return cls.__sql_keywords.not_exists()  

    @classmethod  
    def union(cls):  
        cls._initialize()  
        return cls.__sql_keywords.union()  

    @classmethod  
    def union_all(cls):  
        cls._initialize()  
        return cls.__sql_keywords.union_all()  

    @classmethod  
    def truncate(cls):  
        cls._initialize()  
        return cls.__sql_keywords.truncate()  

    @classmethod  
    def table(cls):  
        cls._initialize()  
        return cls.__sql_keywords.table()  

    @classmethod  
    def drop(cls):  
        cls._initialize()  
        return cls.__sql_keywords.drop()  

    @classmethod  
    def if_(cls):  
        cls._initialize()  
        return cls.__sql_keywords.if_()  

    @classmethod  
    def to_date(cls):  
        cls._initialize()  
        return cls.__sql_keywords.to_date()  


# 在类外部访问静态属性  
## K._initialize()  # 确保初始化  
# print(K.select())  # 输出: SELECT  
# print(K.from_())   # 输出: FROM  
# print(K.where())   # 输出: WHERE  
# print(K.and_())    # 输出: AND  
# print(K.union_all())  # 输出: UNION ALL