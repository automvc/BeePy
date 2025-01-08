'''
sql语句中没有表的字段，将会报错。
'''

class Orders5:  
    __tablename__ = 'orders'  

    def __init__(self, id: int = None, name: str = None, price: float = None, quantity: int = None,   
                 customer_id: int = None, order_date: str = None, status: str = None,   
                 shipping_address: str = None, payment_method: str = None, note: str = None):  
        self._id = id  
        self._name = name  
        self._price = price  
        self._quantity = quantity  
        self._customer_id = customer_id  
        self._order_date = order_date  
        self._status = status  
        self._shipping_address = shipping_address  
        self._payment_method = payment_method  
        self._note = note  

    # Getter 和 Setter 方法  
    @property  
    def id(self):  
        return self._id  

    @id.setter  
    def id(self, value):  
        self._id = value  

    @property  
    def name(self):  
        return self._name  

    @name.setter  
    def name(self, value):  
        self._name = value  

    @property  
    def price(self):  
        return self._price  

    @price.setter  
    def price(self, value):  
        self._price = value  

    @property  
    def quantity(self):  
        return self._quantity  

    @quantity.setter  
    def quantity(self, value):  
        self._quantity = value  

    @property  
    def customer_id(self):  
        return self._customer_id  

    @customer_id.setter  
    def customer_id(self, value):  
        self._customer_id = value  

    @property  
    def order_date(self):  
        return self._order_date  

    @order_date.setter  
    def order_date(self, value):  
        self._order_date = value  

    @property  
    def status(self):  
        return self._status  

    @status.setter  
    def status(self, value):  
        self._status = value  

    @property  
    def shipping_address(self):  
        return self._shipping_address  

    @shipping_address.setter  
    def shipping_address(self, value):  
        self._shipping_address = value  

    @property  
    def payment_method(self):  
        return self._payment_method  

    @payment_method.setter  
    def payment_method(self, value):  
        self._payment_method = value  

    @property  
    def note(self):  
        return self._note  

    @note.setter  
    def note(self, value):  
        self._note = value  