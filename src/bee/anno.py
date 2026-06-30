from typing import List

from bee.bee_enum import JoinType


class JoinTable:
    '''
    Join Meta for join table.
    <B>since  1.9.0</B><br>
    '''

    def __init__(self, sub_class, joinType:JoinType, main_fields: List[str], sub_fields: List[str], sub_alias:str = None, is_list: bool = None, main_alias:str = None):
        self.sub_class = sub_class
        self.joinType = joinType
        self.main_fields = main_fields
        self.sub_fields = sub_fields
        self.sub_alias = sub_alias
        self.is_list = is_list
        self.main_alias = main_alias
