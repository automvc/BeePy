from abc import ABC, abstractmethod
from typing import List, Set, Any

from bee.context import HoneyContext
from bee.exception import ParamBeeException, BeeErrorGrammarException
from bee.name import NameCheckUtil
from bee.name.naming_handler import NamingHandler
from bee.osql.bee_enum import FunctionType, Op, OrderType, SuidType
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K


# since 1.6.0
class Expression: 

    def __init__(self, field_name: str = None, Op: Op = None, op_type = None, value: Any = None,
                 op_num: int = None, value2: Any = None, value3: Any = None, value4: Any = None): 
        self.field_name = field_name  
        self.op_type = op_type if op_type else Op.get_name() if Op else None  
        self.op = Op  
        self.value = value  
        self.op_num = op_num  # type num
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

    def __init__(self, where: str, pv: List[PreparedValue], values: List, suidType:SuidType, whereFields:Set, selectFields:str, start:int, size:int, has_for_update:bool): 
        self.where = where  
        self.pv = pv
        self.values = values
        self.suidType = suidType
        self.whereFields = whereFields
        self.selectFields = selectFields
        self.start = start
        self.size = size
        self.has_for_update = has_for_update
        
    def __repr__(self):
        return  str(self.__dict__) 

    
class ConditionUpdateSetStruct:

    def __init__(self, updateSet: str, pv: List[PreparedValue], values: List, suidType:SuidType, updateSetFields:Set): 
        self.updateSet = updateSet  
        self.pv = pv
        self.values = values
        self.suidType = suidType
        self.updateSetFields = updateSetFields
        
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
    def start(self, start:int) -> 'Condition': 
        pass
    
    @abstractmethod  
    def forUpdate(self) -> 'Condition': 
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
    
    # ## ###########-------just use in update-------------start-
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
    def setWithField(self, field1: str, field2: str) -> 'Condition': 
        pass 
    
    @abstractmethod  
    def setNull(self, field: str) -> 'Condition': 
        pass
    
    # ## ###########-------just use in update-------------end-


class ConditionImpl(Condition):

    def __init__(self): 
        self.expressions = []  # List of Expression objects  
        self.where_fields = set()  # Fields used in WHERE clause 
        
        self.update_set_exp = []
        self.update_set_fields = set()
        
        self.__isStartOrderBy = True
        self.__isStartGroupBy = True
        self.__isStartHaving = True
        self.__suidType = SuidType.SELECT
        
    def __check_one_field(self, field):
        NameCheckUtil._check_one_name(field)

    def op(self, field: str, Op: Op, value: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, Op = Op, value = value, op_num = 2)  
        self.expressions.append(exp)  
        self.where_fields.add(field)  
        return self  

    def and_(self) -> 'ConditionImpl': 
        exp = Expression(op_type = K.and_(), op_num = 1)  
        self.expressions.append(exp) 
        return self  

    def or_(self) -> 'ConditionImpl': 
        exp = Expression(op_type = K.or_(), op_num = 1)  
        self.expressions.append(exp)
        return self  

    def not_(self) -> 'ConditionImpl': 
        exp = Expression(op = Op.eq, op_type = K.not_(), op_num = 1)  
        self.expressions.append(exp)  
        return self  

    def l_parentheses(self) -> 'ConditionImpl': 
        exp = Expression(value = "(", op_num = -2)  
        self.expressions.append(exp)  
        return self  

    def r_parentheses(self) -> 'ConditionImpl': 
        exp = Expression(value = ")", op_num = -1)
        self.expressions.append(exp)  
        return self  

    def between(self, field: str, low: Any, high: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, op_type = K.between(), value = low, value2 = high, op_num = 3)  
        self.expressions.append(exp)  
        self.where_fields.add(field)  
        return self
    
    def opWithField(self, field: str, op: Op, field2: str) -> 'ConditionImpl':
        self.__check_one_field(field) 
        self.__check_one_field(field2)
        expr = Expression(field_name = field, Op = op, value = field2, op_num = -3)  
        self.expressions.append(expr)  
        self.where_fields.add(field)
        return self  
    
    # 'forUpdate', 'groupBy', 'orderBy', 'selectField', 'size', 'start'

    def groupBy(self, field:str) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, op_type = K.group_by(), op_num = -4)
        
        if self.__isStartGroupBy:
            self.__isStartGroupBy = False
            exp.value = K.group_by()
        else:
            exp.value = self.COMMA 
        self.expressions.append(exp) 
        return self
    
    # having(FunctionType.MIN, "field", Op.ge, 60)-->having min(field)>=60
    def having(self, functionType:FunctionType, field: str, op: Op, value: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, Op = op, value = value, op_num = 5)
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
        self.__check_one_field(field)
        exp = Expression(field_name = field, op_type = K.order_by(), op_num = 12)
        self.expressions.append(exp) 
        if self.__isStartOrderBy:
            self.__isStartOrderBy = False
            exp.value = K.order_by()
        else:
            exp.value = self.__COMMA
        return self
    
    def orderBy2(self, field:str, orderType:OrderType) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, op_type = K.order_by(), op_num = 13)
        exp.value2 = orderType.get_name()
        self.expressions.append(exp) 
        if self.__isStartOrderBy:
            self.__isStartOrderBy = False
            exp.value = K.order_by()
        else:
            exp.value = self.__COMMA
        return self
    
    def orderBy3(self, functionType:FunctionType, field:str, orderType:OrderType) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, op_type = K.order_by(), op_num = 14)
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
        if fields:
            if len(fields) == 1:
                if fields[0]:
                    NameCheckUtil.check_fields(fields[0].replace(" ",""))
            else:
                for field in fields:
                    self.__check_one_field(field)
        exp = Expression(value = fields, op_num = 20)
        self.expressions.append(exp)
        return self
    
    def start(self, start:int) -> 'ConditionImpl': 
        # 　if not 0:　is True
        if start is None or start == '' or start < 0:
            raise ParamBeeException("Parameter 'start' need >=0 .")
        exp = Expression(value = start, op_num = 21)
        self.expressions.append(exp)
        return self
    
    def size(self, size:int) -> 'ConditionImpl': 
        if not size or size <= 0:
            raise ParamBeeException("Parameter 'size' need >0 .")
        
        exp = Expression(value = size, op_num = 22)
        self.expressions.append(exp)
        return self
    
    def forUpdate(self) -> 'ConditionImpl':
        exp = Expression(op_type = K.for_update(), op_num = 30)
        self.expressions.append(exp)
        return self
    
    def suidType(self, suidType:SuidType) -> 'ConditionImpl': 
        self.__suidType = suidType
        return self
    
    # get
    def getSuidType(self) -> 'SuidType': 
        return self.__suidType
    
    # ## ###########-------just use in update set-------------start-
    # salary = salary + 1000  
    def setAdd(self, field: str, value: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, value = value, op_num = 52, op_type = "+")
        self.update_set_exp.append(exp)
        self.update_set_fields.add(field)
        return self
    
    # salary = salary * 1.1  
    def setMultiply(self, field: str, value: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, value = value, op_num = 53, op_type = "*")
        self.update_set_exp.append(exp)  
        self.update_set_fields.add(field)  
        return self  
    
    def setAdd2(self, field1: str, field2: str) -> 'ConditionImpl': 
        self.__check_one_field(field1)
        self.__check_one_field(field2)
        exp = Expression(field_name = field1, value = field2, op_num = 54, op_type = "+")
        self.update_set_exp.append(exp)  
        self.update_set_fields.add(field1)  
        self.update_set_fields.add(field2)  
        return self   
    
    def setMultiply2(self, field1: str, field2: str) -> 'ConditionImpl': 
        self.__check_one_field(field1)
        self.__check_one_field(field2)
        exp = Expression(field_name = field1, value = field2, op_num = 55, op_type = "*")
        self.update_set_exp.append(exp)  
        self.update_set_fields.add(field1)  
        self.update_set_fields.add(field2)  
        return self  
    
    def set(self, field: str, value: Any) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, value = value, op_num = 60)
        self.update_set_exp.append(exp)
        self.update_set_fields.add(field)
        return self
    
    # setWithField(field1,field2)--> set field1 = field2
    def setWithField(self, field1: str, field2: str) -> 'ConditionImpl': 
        self.__check_one_field(field1)
        self.__check_one_field(field2)
        exp = Expression(field_name = field1, value = field2, op_num = 61)
        self.update_set_exp.append(exp)  
        self.update_set_fields.add(field1)  
        self.update_set_fields.add(field2)  
        return self
    
    def setNull(self, field: str) -> 'ConditionImpl': 
        self.__check_one_field(field)
        exp = Expression(field_name = field, value = None, op_num = 62)
        self.update_set_exp.append(exp)
        self.update_set_fields.add(field)
        return self

    # ## ###########-------just use in update set-------------end-
    
    # parse where
    def parseCondition(self) -> ConditionStruct:
        return ParseCondition.parse(self.expressions, self)
    
    # parse update set
    def parseConditionUpdateSet(self) -> ConditionUpdateSetStruct:
        return ParseCondition.parseUpdateSet(self.update_set_exp, self)

    
class ParseCondition:
    
    @staticmethod
    def __getPlaceholder() -> str:
        return HoneyContext.get_placeholder() 
    
    # parse update set
    @staticmethod       
    def parseUpdateSet(expressions, condition:Condition) -> ConditionUpdateSetStruct:
        update_set_sql = []
        prepared_values = []
        values = []
        COMMA = ","
          
        is_first = True
        suidType = condition.getSuidType()  
        ph = ParseCondition.__getPlaceholder()  
        
        for exp in expressions:
            
            if is_first:
                is_first = False
            else:
                update_set_sql.append(COMMA)
            
            column_name = NamingHandler.toColumnName(exp.field_name)
            
            # salary = salary * 1.1
            # salary = salary + 1000
            if exp.op_num == 52 or exp.op_num == 53:
                clause = f"{column_name} = {column_name} {exp.op_type} {ph}"
                update_set_sql.append(clause) 
                prepared_values.append(PreparedValue(type(exp.value), exp.value)) 
                values.append(exp.value)
                
            # SET salary = salary + bonus;
            elif exp.op_num == 54 or exp.op_num == 55:
                clause = f"{column_name} = {column_name} {exp.op_type} {exp.value}"
                update_set_sql.append(clause)
               
            # manager_id = 1 
            elif exp.op_num == 60:
                clause = f"{column_name} = {ph}"
                update_set_sql.append(clause) 
                prepared_values.append(PreparedValue(type(exp.value), exp.value)) 
                values.append(exp.value)
                
            # salary = bonus  #61
            # remark = null   #62
            elif exp.op_num == 61 or exp.op_num == 62:
                clause = f"{column_name} = {exp.value}"
                update_set_sql.append(clause)

            elif exp.op_num == -2:  # Left parenthesis
                update_set_sql.append("(")  
            elif exp.op_num == -1:  # Right parenthesis  
                update_set_sql.append(")")  

            else: 
                Logger.warn(f"Unknown operation number: {exp.op_num}")  
                
# UPDATE employees  
# SET salary = 60000, department = 'HR'  
# WHERE employee_id = 101;      
                
# UPDATE employees  
# SET salary = CASE  
#     WHEN department = 'Sales' THEN salary * 1.2  
#     WHEN department = 'HR' THEN salary * 1.1  
#     ELSE salary  
# END; 

# UPDATE employees e  
# JOIN departments d ON e.department_id = d.department_id  
# SET e.salary = e.salary * 1.1  
# WHERE d.department_name = 'Engineering'; 

# UPDATE employees  
# SET salary = (  
#     SELECT AVG(salary)  
#     FROM employees  
#     WHERE department = 'HR'  
# )  
# WHERE employee_id = 102;  

# 6. 使用ORDER BY和LIMIT：限制更新数量
# 按特定顺序更新前N行（适用于MySQL等支持的数据库）。
#
# sql
# UPDATE scores  
# SET score = 100  
# ORDER BY submission_time DESC  
# LIMIT 5;   

        # Join all where clauses into a single string  
        updateSet_str = "".join(update_set_sql)  

        return ConditionUpdateSetStruct(updateSet_str, prepared_values, values, suidType, condition.update_set_fields) 
    
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
            if exp.op_num == 2:  # Binary operation  # op("name", Op.ne, "bee1")
                is_need_and = adjust_and()
                if exp.value is None:
                    where_clause = f"{column_name} {K.isnull()}"
                else:
                    where_clause = f"{column_name} {exp.op} {ph}"
                    prepared_values.append(PreparedValue(type(exp.value), exp.value)) 
                    values.append(exp.value)
                where_clauses.append(where_clause) 
                is_need_and = True
                
            elif exp.op_num == -3:  # eg:field1=field2
                is_need_and = adjust_and()
                where_clause = f"{column_name} {exp.op} {exp.value}"
                where_clauses.append(where_clause)  
                is_need_and = True
                
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
                
            elif exp.op_num == 3:  # BETWEEN  
                is_need_and = adjust_and()
                where_clause = f"{column_name} {exp.op_type} {ph} {K.and_()} {ph}"
                where_clauses.append(where_clause)  
                prepared_values.append(PreparedValue(type(exp.value), exp.value))
                prepared_values.append(PreparedValue(type(exp.value), exp.value2)) 
                values.append(exp.value)
                values.append(exp.value2) 
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
                    where_clauses.append(" ")
                    where_clauses.append(exp.value2)

            elif exp.op_num == 20:  # selectField("name,age")
                __selectFields = exp.value
                
            elif exp.op_num == 21:  # start
                __start = exp.value 
            elif exp.op_num == 22:  # size
                __size = exp.value
                
            elif exp.op_num == 30:  # for update
                __has_for_update = True
            else: 
                Logger.warn(f"Unknown operation number: {exp.op_num}")  

        # Join all where clauses into a single string  
        where_clause_str = "".join(where_clauses)  

        return ConditionStruct(where_clause_str, prepared_values, values, suidType, condition.where_fields, __selectFields, __start, __size, __has_for_update)

