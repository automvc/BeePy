from bee.config import HoneyConfig
from bee.custom import Custom
from bee.name.naming_handler import NamingHandler
from bee.osql.const import SysConst, DatabaseConst
from bee.osql.logger import Logger
from bee.osql.mid_typing import Column
from bee.osql.type_transform import Py2Sql, Sql2Py, Mid


class HoneyUtil:
    '''
    Util for Bee framework.
    '''

    @staticmethod
    def get_obj_field_value(obj):
        # 返回给定对象的属性字典，如果没有则返回None
        """Return the property dictionary of the given object, if not, return None"""

        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return None

    @staticmethod
    def get_class_field_value(clazz):

        if hasattr(clazz, '__dict__'):
            # 并去掉前缀__和_   只是__开头，会变化的。
            class_name = clazz.__name__
            prefix = "_" + class_name + "__"
            kv = { key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key: value
                   for key, value in clazz.__dict__.items() if not (key.startswith('__') and key.endswith('__'))}
            for key, value in kv.items():
                if isinstance(value, property):
                    kv[key] = None  # 使用get/set,暂时不能获取到bean的类级别的值。
                    # kv[key]=getattr(clazz, key)
                elif isinstance(value, Column):
                    # print(value)
                    kv[key] = None
            return kv
        else:
            return None

        # result = {}
        # for key in cls.__class__.__dict__:
        #     # 排除私有属性
        #     if not (key.startswith('__') and key.endswith('__')):
        #         value = getattr(cls, key)
        #         # 如果是property类型，则获取其值
        #         if isinstance(value, property):
        #             result[key] = getattr(cls, key)  # 通过实例获取属性值
        #         else:
        #             result[key] = value
        # print(result)
        # return result
    # dict: {'id': <property object at 0x000001E2C878D350>, 'name': <property object at 0x000001E2C878D3A0>, 'remark': <property object at 0x000001E2C878D3F0>}

    @staticmethod
    def get_class_field(clazz):
        # 返回给定类的属性列表,但不包括系统的
        # since 1.6.0 还考虑字段的类型,时间类型等
        """
        Returns a list of properties for a given class, but does not include the system's.
        """
        fieldname_and_type_dict = HoneyUtil.get_field_and_type(clazz)
        return list(fieldname_and_type_dict.keys())

    # 对象的不会改
    @staticmethod
    def remove_prefix(dict_obj):
        """ remove  __  or _ prefix """
        if not dict_obj:
            return dict_obj

        fieldAndValue = {
            key[2:] if key.startswith('__') else key[1:] if key.startswith('_') else key: value
            for key, value in dict_obj.items()
        }
        return fieldAndValue

    @staticmethod
    def get_list_params(classField, entity_list):
        # 获取对象的值元列表
        """
        get object value with tuple.
        eg:
                # list_params = [<br>
                #     (None, 'Alice', 30, 'Likes swimming', '123 Maple St'),<br>
                #     (None, 'Charlie', 35, 'Enjoys hiking', None),<br>
                #     (None, 'David', 28, None, None),  # remark 和 addr 均为空  <br>
                #     ] <br>
        """

        dict_n = {e: None for e in classField}
        # dict_classField=dict_n.copy()

        list_params = []
        for entity in entity_list:
            obj_dict = HoneyUtil.get_obj_field_value(entity)
            dict_classField = dict_n.copy()
            for k, v in obj_dict.items():
                if v is not None and k in dict_classField:
                    dict_classField[k] = v
            list_params.append(tuple(dict_classField.values()))

        return list_params

    @staticmethod
    def get_table_name(obj):
        cls = obj.__class__
        return HoneyUtil.get_table_name_by_class(cls)

    @staticmethod
    def get_table_name_by_class(clazz):
        # clazz = obj.__class__
        temp_name = getattr(clazz, '__tablename__', None)
        # temp_name
        if temp_name and not temp_name.isspace():
            return temp_name.strip()
        class_name = clazz.__name__
        return NamingHandler.toTableName(class_name)

    @staticmethod
    def get_pk(obj):
        cls = obj.__class__
        return HoneyUtil.get_pk_by_class(cls)

    @staticmethod
    def get_pk_by_class(clazz):
        """ get pk from bean"""
        temp_name = getattr(clazz, SysConst.pk, None)
        if temp_name and not temp_name.isspace():
            return temp_name.strip()
        else:
            temp_name = getattr(clazz, SysConst.primary_key, None)
            if temp_name and not temp_name.isspace():
                return temp_name.strip()
            else:
                if hasattr(clazz, SysConst.id):
                    return SysConst.id
        return None

    @staticmethod
    def get_unique_key(clazz):
        return getattr(clazz, SysConst.unique_key, None)

    @staticmethod
    def get_not_null_filels(clazz):
        return getattr(clazz, SysConst.not_null_filels, None)

    @staticmethod
    def is_sql_key_word_upper():
        if HoneyConfig.sql_key_word_case:
            if HoneyConfig.sql_key_word_case == SysConst.upper:
                return True
        return False

    @staticmethod
    def generate_pk_statement():
        dbname = HoneyConfig().get_dbname()
        if dbname == DatabaseConst.MYSQL.lower():
            return " INT PRIMARY KEY AUTO_INCREMENT NOT NULL"
        elif dbname == DatabaseConst.SQLite.lower():
            return " INTEGER PRIMARY KEY NOT NULL"  # 自动增长
        elif dbname == DatabaseConst.ORACLE.lower():
            return " NUMBER PRIMARY KEY"
        elif dbname == DatabaseConst.PostgreSQL.lower():
            return " SERIAL PRIMARY KEY"
        else:
            # Logger.warn(f"Unsupported database type: {dbname}, when generate primary key!")
            Logger.warn(f"There is not dedicated primary key statement for: {dbname}, will use normal!")
            temp = " " + Custom.custom_pk_statement()
            # if column:
            #     temp += ",\n    PRIMARY KEY(" + column + ")"
            return temp
            # raise ValueError(f"Unsupported database type: {dbname}")

    @staticmethod
    def adjustUpperOrLower(value):
        if not value:
            return value
        isUpper = HoneyUtil.is_sql_key_word_upper()
        if isUpper:
            return value.upper()
        else:
            return value.lower()

    @staticmethod
    def python_type_to_sql_type(python_type):
        type0 = Py2Sql().python_type_to_sql_type(python_type)
        return HoneyUtil.adjustUpperOrLower(type0)

    @staticmethod
    def sql_type_to_python_type(sql_type):
        return Sql2Py().sql_type_to_python_type(sql_type)

    @staticmethod
    def mid_type_to_sql_type(mid_type):
        mid = Mid()
        # 直接找到，则直接返回
        sql_type = mid.mid_to_sqltype(mid_type)
        if sql_type:
            return sql_type

        python_type = mid.mid_to_python_type(mid_type)

        type0 = Py2Sql().python_type_to_sql_type(python_type)
        return HoneyUtil.adjustUpperOrLower(type0)

    @staticmethod
    def get_class_normal_field(clazz):
        if hasattr(clazz, '__dict__'):
            # 过滤掉以__开头和结尾的键，并去掉前缀__和_   只是__开头，会变化的。
            class_name = clazz.__name__
            prefix = "_" + class_name + "__"
            return [
                key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key
                for key in clazz.__dict__.keys()
                if not (key.startswith('__') and key.endswith('__'))
            ]
        else:
            return None

    __field_and_type_cache = {}  # V1.6.0

    @staticmethod
    def get_field_and_type(clazz):
        field_and_type = HoneyUtil.__field_and_type_cache.get(clazz, None)
        if field_and_type is None:
            field_and_type = HoneyUtil.__get_field_and_type(clazz)
            HoneyUtil.__field_and_type_cache[clazz] = field_and_type
        return field_and_type

    @staticmethod
    def __get_field_and_type(clazz):
        # 声明基本类型和无声明类型的字段（保留定义顺序）
        A = HoneyUtil.get_class_normal_field(clazz)

        B = {}
        try:
            # 保留有类型的, 包括复合类型, 低版本没有使用时，会报异常
            # 3.8.10 have exception if no use like: remark: str = None
            B = clazz.__annotations__
        except Exception:
            pass

        M = HoneyUtil.get_mid_field_and_type(clazz)
        # print(M)
        if M:
            if not B:
                B = M
            else:
                B.update(M)

        # 保留有类型的, 包括复合类型
        # B = clazz.__annotations__  #3.8.10 have exception if no use like: remark: str = None
        new_map = {}

        # none_type_set=set(A)-set(B)
        # 复合类型  complex_type_set
        ext = set(B) - set(A)  # 两个类型是一样的吗？

        if not ext:
            for f in A:
                if f in B:
                    # a1.声明类型的
                    new_map[f] = B[f]
                else:
                    # a2.无类型声明
                    new_map[f] = None
        else:
            # A=A
            # B=B
            # ext=complex_type_set
            B_keys = list(B.keys())

            # 使用简单的索引方式遍历 A 和 B
            i, j = 0, 0
            len_A, len_B = len(A), len(B_keys)

            # 可以保证基本类型与无类型混合时的原始顺序
            while i < len_A and j < len_B:
                # b1.声明类型的
                if A[i] == B_keys[j]:
                    new_map[B_keys[j]] = B[B_keys[j]]
                    i += 1
                    j += 1
                # b2.复合类型
                elif B_keys[j] in ext:
                    new_map[B_keys[j]] = B[B_keys[j]]
                    j += 1
                # b3.无类型声明
                else:
                    new_map[A[i]] = None
                    i += 1

            while i < len_A:
                new_map[A[i]] = None
                i += 1

            while j < len_B:
                new_map[B_keys[j]] = B[B_keys[j]]
                j += 1

            # 无声明类型与复合类型邻近，则无法识别；默认先处理复合类型(b2->b3)
            # descstr=None
            # modify_date: date
            # updated_at2: date
            # 结果变为：
            # modify_date DATE,
            # updated_at2 DATE,
            # descstr VARCHAR(255)
        # print("-----1111------")
        # print(new_map)
        return new_map

    @staticmethod
    def get_field_type(clazz, fieldname):
        field_and_type = HoneyUtil.get_field_and_type(clazz)
        if field_and_type:
            return field_and_type.get(fieldname, None)
        else:
            return None

    @staticmethod
    def get_mid_field_and_type(clazz):
        m = {}
        for name, obj in clazz.__dict__.items():
            if isinstance(obj, Column):  # 确认是Column对象
                field_type = obj.type
                # print(f"字段名: {name}, 类型: {field_type}")
                m[name] = Mid().mid_to_python_type(str(field_type))
        return m

    @staticmethod
    def get_type(param):
        # 1. 传入的是类型（包括内建 type 子类）
        if isinstance(param, type):
            return param

        # # 2. 传入的是 typing 泛型（Python3.8+ 的 typing 对象或 3.9+ 的内置泛型）
        # #    get_origin 在非泛型对象上返回 None
        # origin = get_origin(x)
        # if origin is not None:
        #     return origin

        # 3. 否则认为是实例，返回其实例类型
        return type(param)

