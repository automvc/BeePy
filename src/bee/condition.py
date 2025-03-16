from abc import ABC, abstractmethod  
from typing import List, Any  

from bee.context import HoneyContext
from bee.exception import ParamBeeException, BeeErrorGrammarException
from bee.name.naming_handler import NamingHandler
from bee.osql.enum import FunctionType, Op, OrderType, SuidType
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K

#since 1.6.0
class Expression: 

    def __init__(self, field_name: str=None, Op: Op=None, op_type=None, value: Any=None,
                 op_num: int=None, value2: Any=None, value3: Any=None, value4: Any=None): 
        self.field_name = field_name  
        self.op_type = op_type if op_type else Op.get_name() if Op else None  
        self.op = Op  
        self.value = value  
        self.op_num = op_num  # if op_num is not None else 2  # Default for binary operations  
        self.value2 = value2  
        self.value3 = value3  
        self.value4 = value4  

    def __str__(self): 
        if self.op_num == 2:  # Binary operation  
            return f"{self.field_name} {self.op} {self.value}"  
        else: 
            return str(self.__dict__)


class PreparedValue:

    def __init__(self, typeStr: str, value: Any): 
        self.typeStr = typeStr  
        self.value = value
        
    def __repr__(self):
        return  str(self.__dict__)

    
class ConditionStruct:

    def __init__(self, where: str, pv: List[PreparedValue], values: List, suidType:SuidType, selectFields:str, start:int, size:int, has_for_update:bool): 
        self.where = where  
        self.pv = pv
        self.values = values
        self.suidType = suidType
        self.selectFields = selectFields
        self.start = start
        self.size = size
        self.has_for_update = has_for_update
        
    def __repr__(self):
        return  str(self.__dict__) 
    
class ConditionUpdateSetStruct:

    def __init__(self, updateSet: str, pv: List[PreparedValue], values: List, suidType:SuidType): 
        self.updateSet = updateSet  
        self.pv = pv
        self.values = values
        self.suidType = suidType

        
    def __repr__(self):
        return  str(self.__dict__) 


class Condition(ABC): 

    @abstractmethod  
    def op(self, field: str, Op: Op, value: Any) -> 'Condition': 
        pass 
    
    @abstractmethod  
    def opWithField(self, field: str, op: Op, field2: str) -> 'Condition': 
        pass

    @abstractmethod  
    def and_(self) -> 'Condition': 
        pass  

    @abstractmethod  
    def or_(self) -> 'Condition': 
        pass  

    @abstractmethod  
    def not_(self) -> 'Condition': 
        pass  

    @abstractmethod  
    def l_parentheses(self) -> 'Condition': 
        pass  

    @abstractmethod  
    def r_parentheses(self) -> 'Condition': 
        pass  

    @abstractmethod  
    def between(self, field: str, low: Any, high: Any) -> 'Condition': 
        pass  
    
    @abstractmethod  
    def groupBy(self, field:str) -> 'Condition': 
        pass
    
    @abstractmethod  
    def having(self, functionType:FunctionType, field: str, op: Op, value: Any) -> 'Condition': 
        pass
    
    @abstractmethod  
    def orderBy(self, field:str) -> 'Condition': 
        pass

    @abstractmethod  
    def orderBy2(self, field:str) -> 'Condition': 
        pass

    @abstractmethod  
    def orderBy3(self, field:str) -> 'Condition': 
        pass
    
    @abstractmethod  
    def selectField(self, *field:str) -> 'Condition': 
        pass
    
    @abstractmethod  
    def forUpdate(self) -> 'Condition': 
        pass
    
    @abstractmethod  
    def start(self, start:int) -> 'Condition': 
        pass
    
    @abstractmethod  
    def size(self, size:int) -> 'Condition': 
        pass
    
    @abstractmethod  
    def suidType(self, suidType:SuidType) -> 'Condition': 
        pass
    
    @abstractmethod  
    def getSuidType(self) -> 'Condition': 
        pass
    
    ### ###########-------just use in update-------------start-
    @abstractmethod  
    def setAdd(self, field: str, value: Any) -> 'Condition': 
        pass 
    
    @abstractmethod  
    def setMultiply(self, field: str, value: Any) -> 'Condition': 
        pass
    
    @abstractmethod  
    def setAdd2(self, field1: str, field2: str) -> 'Condition': 
        pass 
    
    @abstractmethod  
    def setMultiply2(self, field1: str, field2: str) -> 'Condition': 
        pass
    
    @abstractmethod  
    def set(self, field: str, value: Any) -> 'Condition': 
        pass 
    
    @abstractmethod  
    def setNull(self, field: str) -> 'Condition': 
        pass
    
    @abstractmethod  
    def setWithField(self, field1: str, field2: str) -> 'Condition': 
        pass 
    ### ###########-------just use in update-------------end-

class ConditionImpl(Condition):

    def __init__(self): 
        self.expressions = []  # List of Expression objects  
        self.where_fields = set()  # Fields used in WHERE clause 
        
        self.update_set_exp = []
        self.update_set_fields = set()
        
        self.__isStartOrderBy = True  # 实例变量  
        self.__isStartGroupBy = True
        self.__isStartHaving = True
        self.__suidType = SuidType.SELECT
        
    def __check_field(self, field):
        pass  # TODO

    def op(self, field: str, Op: Op, value: Any) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, Op=Op, value=value, op_num=2)  
        self.expressions.append(exp)  
        self.where_fields.add(field)  
        return self  

    def and_(self) -> 'ConditionImpl': 
        exp = Expression(op_type=K.and_(), op_num=1)  
        self.expressions.append(exp) 
        return self  

    def or_(self) -> 'ConditionImpl': 
        exp = Expression(op_type=K.or_(), op_num=1)  
        self.expressions.append(exp)
        return self  

    def not_(self) -> 'ConditionImpl': 
        exp = Expression(op=Op.eq, op_type=K.not_(), op_num=1)  
        self.expressions.append(exp)  
        return self  

    def l_parentheses(self) -> 'ConditionImpl': 
        exp = Expression(value="(", op_num=-2)  
        self.expressions.append(exp)  
        return self  

    def r_parentheses(self) -> 'ConditionImpl': 
        exp = Expression(value=")", op_num=-1)
        self.expressions.append(exp)  
        return self  

    def between(self, field: str, low: Any, high: Any) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, op_type=K.between(), value=low, value2=high, op_num=3)  
        self.expressions.append(exp)  
        self.where_fields.add(field)  
        return self
    
    def opWithField(self, field: str, op: Op, field2: str) -> 'ConditionImpl':
        self.__check_field(field) 
        self.__check_field(field2)
        expr = Expression(field_name=field, Op=op, value=field2, op_num=-3)  
        self.expressions.append(expr)  
        self.where_fields.add(field)
        return self  
    
    # 'forUpdate', 'groupBy', 'orderBy', 'selectField', 'size', 'start'

    def groupBy(self, field:str) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, op_type=K.group_by(), op_num=-4)
        
        if self.__isStartGroupBy:
            self.__isStartGroupBy = False
            exp.value = K.group_by()
        else:
            exp.value = self.COMMA 
        self.expressions.append(exp) 
        return self
    
    # having(FunctionType.MIN, "field", Op.ge, 60)-->having min(field)>=60
    def having(self, functionType:FunctionType, field: str, op: Op, value: Any) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, Op=op, value=value, op_num=5)
        exp.value2 = functionType
        
        if self.__isStartHaving:
            if self.__isStartGroupBy:
                Logger.warn("The 'having' must be after 'group by'!")
            self.__isStartHaving = False
            exp.op_type = K.having()
        else:
            exp.op_type = K.and_()
          
        self.expressions.append(exp)  
        self.where_fields.add(field)  
        return self  
    
    __COMMA = ","

    def orderBy(self, field:str) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, op_type=K.order_by(), op_num=12)
        self.expressions.append(exp) 
        if self.__isStartOrderBy:
            self.__isStartOrderBy = False
            exp.value = K.order_by()
        else:
            exp.value = self.__COMMA
        return self
    
    def orderBy2(self, field:str, orderType:OrderType) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, op_type=K.order_by(), op_num=13)
        exp.value2 = orderType.get_name()
        self.expressions.append(exp) 
        if self.__isStartOrderBy:
            self.__isStartOrderBy = False
            exp.value = K.order_by()
        else:
            exp.value = self.__COMMA
        return self
    
    def orderBy3(self, functionType:FunctionType, field:str, orderType:OrderType) -> 'ConditionImpl': 
        self.__check_field(field)
        exp = Expression(field_name=field, op_type=K.order_by(), op_num=14)
        exp.value2 = orderType.get_name()
        exp.value3 = functionType.get_name()
        self.expressions.append(exp) 
        if self.__isStartOrderBy:
            self.__isStartOrderBy = False
            exp.value = K.order_by()
        else:
            exp.value = self.__COMMA
        return self
    
    def selectField(self, *fields:str) -> 'ConditionImpl': 
        self.__check_field(fields)
        exp = Expression(value=fields, op_num=20)
        self.expressions.append(exp)
        return self
    
    def start(self, start:int) -> 'ConditionImpl': 
        if start is None or start < 0:   #　if not 0:　is True
            raise ParamBeeException("Parameter 'start' need >=0 .")
        exp = Expression(value=start, op_num=21)
        self.expressions.append(exp)
        return self
    
    def size(self, size:int) -> 'ConditionImpl': 
        if not size or size <= 0:
            raise ParamBeeException("Parameter 'size' need >0 .")
        
        exp = Expression(value=size, op_num=22)
        self.expressions.append(exp)
        return self
    
    def suidType(self, suidType:SuidType) -> 'ConditionImpl': 
        self.__suidType = suidType
        return self
    
    # get
    def getSuidType(self) -> 'SuidType': 
        return self.__suidType
    
    def forUpdate(self) -> 'ConditionImpl':
        exp = Expression(op_type=K.for_update(), op_num=30)
        self.expressions.append(exp)
        return self
    
    ### ###########-------just use in update-------------start-
    def setAdd(self, field: str, value: Any) -> 'ConditionImpl': 
        pass 
    
    def setMultiply(self, field: str, value: Any) -> 'ConditionImpl': 
        pass
    
    def setAdd2(self, field: str, otherFieldName: str) -> 'ConditionImpl': 
        pass 
    
    def setMultiply2(self, field: str, otherFieldName: str) -> 'ConditionImpl': 
        pass
    
    def set(self, field: str, value: Any) -> 'ConditionImpl': 
        pass 
    
    def setNull(self, field: str) -> 'ConditionImpl': 
        pass
    
    def setWithField(self, field1: str, field2: str) -> 'Condition': 
        pass 
    ### ###########-------just use in update-------------end-
    
    
    
    # parse where
    def parseCondition(self) -> ConditionStruct:
        return ParseCondition.parse(self.expressions, self)
    
    # parse update set
    def parseConditionUpdateSet(self) -> ConditionStruct:
        return ParseCondition.parseUpdateSet(self.update_set_exp, self)

    
class ParseCondition:
    
    @staticmethod
    def __getPlaceholder() -> str:
        return HoneyContext.get_placeholder() 
    
    # parse update set
    @staticmethod       
    def parseUpdateSet(update_set_exp, condition:Condition) -> ConditionUpdateSetStruct:
        pass 
    
    # parse where
    @staticmethod       
    def parse(expressions, condition:Condition) -> ConditionStruct: 
        where_clauses = []
        prepared_values = []
        values = []
          
        is_need_and = False
        suidType = condition.getSuidType()  

        def adjust_and() -> bool: 
            nonlocal is_need_and  
            if is_need_and: 
                where_clauses.append(" " + K.and_() + " ")  
                is_need_and = False
                # return False  
            return is_need_and
        
        ph = ParseCondition.__getPlaceholder()  
        
        __has_for_update = False
        __selectFields = None
        __start = None
        __size = None
        for exp in expressions:
            # exp.field_name ->column_name  
            column_name = NamingHandler.toColumnName(exp.field_name)
            if exp.op_num == 2:  # Binary operation 
                is_need_and = adjust_and()
                if exp.value is None:
                    where_clause = f"{column_name} {K.isnull()}"
                else:
                    where_clause = f"{column_name} {exp.op} {ph}"
                    prepared_values.append(PreparedValue(type(exp.value), exp.value)) 
                    values.append(exp.value)
                where_clauses.append(where_clause) 
                is_need_and = True
            elif exp.op_num == 3:  # BETWEEN  
                is_need_and = adjust_and()
                where_clause = f"{column_name} {exp.op_type} {ph} {K.and_()} {ph}"
                where_clauses.append(where_clause)  
                prepared_values.append(PreparedValue(type(exp.value), exp.value))
                prepared_values.append(PreparedValue(type(exp.value), exp.value2)) 
                values.append(exp.value)
                values.append(exp.value2) 
                is_need_and = True
            elif exp.op_num == -3:  # eg:field1=field2
                is_need_and = adjust_and()
                where_clause = f"{column_name} {exp.op} {exp.value}"
                where_clauses.append(where_clause)  
                is_need_and = True
            elif exp.op_num == -4:  # group by
                if suidType != SuidType.SELECT:
                    raise BeeErrorGrammarException(suidType.get_name() + " do not support 'group by' !")
                
                where_clause = f" {exp.value} {column_name}"
                where_clauses.append(where_clause)
                
            elif exp.op_num == 5:  # having
                if suidType != SuidType.SELECT:
                    raise BeeErrorGrammarException(suidType.get_name() + " do not support 'having' !")
                
                where_clause = f" {exp.op_type} {exp.value2.get_name()}({column_name}) {exp.op} {ph}"
                where_clauses.append(where_clause)
                prepared_values.append(PreparedValue(type(exp.value), exp.value)) 
                values.append(exp.value)
                
            elif exp.op_num == 12 or exp.op_num == 13 or exp.op_num == 14:  # order by
                if suidType != SuidType.SELECT:
                    raise BeeErrorGrammarException(suidType.get_name() + " do not support 'order by' !")
                
                where_clauses.append(" " + exp.value + " ")  # order by或者,
                if 14 == exp.op_num:  # order by   max(total)
                    where_clauses.append(exp.value3)
                    where_clauses.append("(")
                    where_clauses.append(column_name)
                    where_clauses.append(")")
                else:
                    where_clauses.append(column_name)

                if 13 == exp.op_num or 14 == exp.op_num:  # 指定 desc,asc
                    where_clauses.append(" ");
                    where_clauses.append(exp.value2)

            elif exp.op_num == 1:  # Logical operator (AND, OR, NOT)
                if exp.op_type == K.not_():
                    is_need_and = adjust_and()
                where_clauses.append(f" {exp.op_type} ")
                is_need_and = False  
            elif exp.op_num == -2:  # Left parenthesis
                is_need_and = adjust_and()   
                where_clauses.append("(")  
            elif exp.op_num == -1:  # Right parenthesis  
                where_clauses.append(")")  
                is_need_and = True
            
            elif exp.op_num == 20:
                __selectFields = exp.value
                
            elif exp.op_num == 21:
                __start = exp.value 
            elif exp.op_num == 22:
                __size = exp.value
                
            elif exp.op_num == 30:  # for update  TODO
                __has_for_update = True
            else: 
                Logger.warn(f"Unknown operation number: {exp.op_num}")  

        # Join all where clauses into a single string  
        where_clause_str = "".join(where_clauses)  

        return ConditionStruct(where_clause_str, prepared_values, values, suidType, __selectFields, __start, __size, __has_for_update)

