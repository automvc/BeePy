# from __future__ import annotations
# from bee.api import SuidRich
# from bee.bee_enum import JoinType
# from bee.honeyfactory import BF
# from bee.osql.gen import GenBean
# from bee.typing import JoinMeta
#
# import MyConfig
#
# class A:
#     """ table s 's entity """
#     id: int = None
#     sname: str = None
#     sno: int = None
#     age: int = None
#
#     x:B=None  #Undefined variable: S
#
#     __joins__ = {}
#
#     def __repr__(self):
#         return str(self.__dict__)
#
# A.__joins__ = {
#     "x": JoinMeta(
#         sub_class=B,            # Undefined variable: B
#         joinType=JoinType.JOIN,
#         main_fields=["id"],
#         sub_fields=["id"],
#         sub_alias='x'
#     )
# }
#
# class B:
#     """ table s 's entity """
#     id: int = None
#     sname: str = None
#     sno: int = None
#     age: int = None
#
#     x:A=None
#
#     __joins__ = {
#     "x": JoinMeta(
#         sub_class=A,
#         joinType=JoinType.JOIN,
#         main_fields=["id"],
#         sub_fields=["id"],
#         sub_alias='x'
#     )
#     }
#
#     def __repr__(self):
#         return str(self.__dict__)
#
#
# if __name__ == '__main__':
#     print("start")
#
#     MyConfig.init()
#
#     # assist =Assist()
#     # assist.get_bean_code("clazz")
#
#     # gen = GenBean()
#     # code=gen.get_bean_code("s") 
#     # print(code)
#
#     s=B()
#     s.sname="WANG"
#
#     moreTable = BF.moreTable()
#     teaList = moreTable.select(s)
#
#     # test can use cache
#     teaList = moreTable.select(s)
#
#     # suidRich = BF.suidRich()
#     # assigncourse = Assigncourse()
#     # assigncourse.teacherno = 1
#     # assigncourse.remark2 = "new remark2"
#     # suidRich.update(assigncourse)
#
#     # test will delete cache after update
#     teaList = moreTable.select(s)
#     print(len(teaList))
#
#     if teaList:
#         for one in teaList:
#             print(one)

