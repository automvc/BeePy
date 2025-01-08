class Orders7:  
    __tablename__ = 'orders'  
    
    def __init__(self, *args, **kwargs):  
        # 使用位置参数设置动态属性  
        for index, value in enumerate(args):  
            setattr(self, f'arg{index}', value)  # 使用动态生成的键  

        # 使用关键字参数更新实例属性  
        for key, value in kwargs.items():  
            setattr(self, key, value)  

# 示例  
# 使用动态参数创建订单实例  
orders1 = Orders7(  
    100001,                  # 算作 arg0   没有字段名，不能用这种形式
    "Bee(ORM Framework)",    # 算作 arg1  
    29.99,                   # 算作 arg2  
    5,                       # 算作 arg3  
    customer_id=123,        # 关键字参数  
    order_date='2023-10-01',# 关键字参数  
    status='Shipped',       # 关键字参数  
    shipping_address='123 Main St', # 关键字参数  
    payment_method='Credit Card',    # 关键字参数  
    note='Leave at the front door'   # 关键字参数  
)  

# 打印实例的属性以验证它们已被设置  
print(vars(orders1))  