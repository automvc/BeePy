from abc import ABC, abstractmethod
from typing import Any

from bee.bee_enum import FunctionType, Op, SuidType, OrderType


class Condition(ABC):
    """
    Condition: used to construct complex WHERE, UPDATE statements and so on.
    """

    @abstractmethod
    def op(self, field: str, op: Op, value: Any) -> 'Condition':
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
    def orderBy2(self, field:str, orderType:OrderType) -> 'Condition':
        pass

    @abstractmethod
    def orderBy3(self, functionType:FunctionType, field:str, orderType:OrderType) -> 'Condition':
        """
        eg: orderBy3(FunctionType.MAX, "total", OrderType.DESC)-->order by max(total) desc
        """

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
    def setAdd(self, field: str, value: int) -> 'Condition':
        pass

    @abstractmethod
    def setMultiply(self, field: str, value: int) -> 'Condition':
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
