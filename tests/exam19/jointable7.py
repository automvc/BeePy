from typing import List, Dict, Type, Any

from bee.api import SuidRich
from bee.bee_enum import JoinType
from bee.honeyfactory import BF
from bee.typing import JoinMeta

import MyConfig
from email._encoded_words import len_q


# from enum import Enum
# class JoinType(Enum):
#     JOIN = "JOIN"
#     LEFT_JOIN = "LEFT JOIN"
#     RIGHT_JOIN = "RIGHT JOIN"
#
#
# # 说明：你给出的 JoinMeta 和模型定义保持不变
# class JoinMeta:
#
#     def __init__(self, sub_class, joinType:JoinType, main_fields: List[str], sub_fields: List[str]):
#         self.sub_class = sub_class
#         self.joinType = joinType
#         self.main_fields = main_fields
#         self.sub_fields = sub_fields
class Teacher:
    classno = None
    term = None
    subjectno = None
    teacherno = None
    remark3=None
    
    def __repr__(self):  
        return  str(self.__dict__)

class Assigncourse:

    teacherno = None
    classno = None
    term = None
    subjectno = None
    examno = None
    remark2=None
    
    def __repr__(self):  
        return  str(self.__dict__)
    

class Assignexam:

    name = None
    classno = None
    term = None
    subjectno = None
    examno = None
    status = None
    teacherno = None
    remark1=None

    # 子表对象  TODO 1: 子表对象不能转到select子句
    assigncourse_aa = None
    teacher_bb = None
    
    def __repr__(self):  
        return  str(self.__dict__)

    __joins__ = {
        "assigncourse_aa": JoinMeta(
            sub_class = Assigncourse,
            joinType = JoinType.JOIN,
            main_fields = ["classno", "term", "subjectno"],
            sub_fields = ["classno", "term", "subjectno"],
        ),
        "teacher_bb": JoinMeta(
            sub_class = Teacher,
            joinType = JoinType.LEFT_JOIN,
            main_fields = ["teacherno"],
            sub_fields = ["teacherno"],
        ),
    }

# -------------- 解析阶段 --------------


def parse_joins(model_cls: Type) -> List[Dict[str, Any]]:
    """
    解析给定模型类中的 __joins__，返回结构化信息列表。
    每个元素包含：
      - attr: 关联属性名
      - sub_class: 子表实体类
      - main_fields: 主表字段列表
      - sub_fields: 子表字段列表
    """
    result: List[Dict[str, Any]] = []
    joins = getattr(model_cls, "__joins__", None)
    if not isinstance(joins, dict):
        return result

    for attr, meta in joins.items():
        if isinstance(meta, JoinMeta):
            item = {
                "attr": attr,
                "sub_class": meta.sub_class,
                "joinType":meta.joinType,
                "main_fields": meta.main_fields,
                "sub_fields": meta.sub_fields,
            }
            result.append(item)
        else:
            # 兼容未来扩展：若有其他类型的元数据对象
            item = {
                "attr": attr,
                "sub_class": getattr(meta, "sub_class", None),
                "joinType":getattr(meta, "joinType", None),
                "main_fields": getattr(meta, "main_fields", []),
                "sub_fields": getattr(meta, "sub_fields", []),
            }
            result.append(item)

    return result

# -------------- JOIN 构建阶段 --------------


def build_join_clause(main_alias: str, joins_info: List[Dict[str, Any]]) -> str:
    """
    根据解析出的 join 信息生成 JOIN 子句。
    假设主表与子表字段通过同名字段进行等值连接，逐条拼接 ON 条件。
    """
    clauses: List[str] = []
    for join in joins_info:
        alias = join["attr"]  # 将子表的表别名设为关联属性名，简单直观
        main_fields = join["main_fields"]
        sub_fields = join["sub_fields"]

        # 组装 ON 条件：m.main_field = alias.sub_field
        on_parts: List[str] = []
        for mf, sf in zip(main_fields, sub_fields):
            on_parts.append(f"{main_alias}.{mf} = {alias}.{sf}")

        on_sql = " AND ".join(on_parts)
        clause = f"{JoinType.JOIN.value} {alias} ON {on_sql}"
        clauses.append(clause)
    return " ".join(clauses)

# def build_from_clause(main_table: str, main_alias: str, joins_info: List[Dict[str, Any]]) -> str:
#     """
#     组成完整的 FROM / JOIN 子句的起始部分
#     """
#     # FROM main_table AS main_alias
#     return f"{main_table} AS {main_alias}"
#
#
# def qualify_column(table_alias: str, column: str) -> str:
#     return f"{table_alias}.{column}"
#
#
# def generate_select_sql(
#     base_table: str,
#     base_alias: str,
#     joins_model_cls: Type,
#     selected_main_fields: Optional[List[str]] = None,
#     where_clause: Optional[str] = None
# ) -> str:
#     """
#     生成一个完整的 SELECT SQL，包括 JOIN。
#     - base_table: 主表名
#     - base_alias: 主表别名
#     - joins_model_cls: 具有 __joins__ 的模型类，用于解析 JOIN 信息
#     - selected_main_fields: 明确需要查询的主表字段（若 None，将默认查询主表所有字段：base_alias.*）
#     - where_clause: 可选的 WHERE 条件字符串，示例："m.classno = 1"
#     """
#     joins_info = parse_joins(joins_model_cls)
#
#     # 选择字段
#     if selected_main_fields is None:
#         main_select = f"{base_alias}.*"
#     else:
#         main_select = ", ".join([f"{base_alias}.{fld}" for fld in selected_main_fields])
#
#     return main_select
#
#     # 如果需要显示子表字段，可以在


# 使用示例
# if __name__ == "__main__":
#     info = parse_joins(Assignexam)
#     for item in info:
#         print(f"关联属性: {item['attr']}")
#         print(f"  sub_class: {item['sub_class']}")
#         print(f"  joinType: {item['joinType']}")
#         print(f"  main_fields: {item['main_fields']}")
#         print(f"  sub_fields: {item['sub_fields']}")
#         print()
        
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    assignexam=Assignexam()
    assignexam.name='Test'
    
    moreTable = BF.moreTable()
    teaList = moreTable.select(assignexam)
    
    print(len(teaList))
    
    if teaList: 
        for one in teaList: 
            print(one)
            
    # suidRich = SuidRich()
    # suidRich.create_table(Assignexam, True)
    # suidRich.create_table(Teacher, True)
    # suidRich.create_table(Assigncourse, True)
    
