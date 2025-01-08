
class Orders6:  
    __tablename__ = 'orders' 
    
    id = None  
    name = None 
    remark = None 

    def __init__(self, **kwargs): 
        # 使用 set 方法动态设置属性  
        for key, value in kwargs.items():  
            setattr(self, key, value)  
            
    def __repr__(self):  
        return  str(self.__dict__)

# 示例  
# 创建订单实例  
order_data = {  
    'id': 100001,  
    'name': "Bee(ORM Framework)",  
    'price': 29.99,  
    'quantity': 5,  
    'customer_id': 123,  
    'order_date': '2023-10-01',  
    'status': 'Shipped',  
    'shipping_address': '123 Main St',  
    'payment_method': 'Credit Card',  
    'note': 'Leave at the front door'  
}  

orders6 = Orders6(**order_data)  

# 打印实例的属性以验证它们已被设置  
print(vars(orders6))