from bee.config import PreConfig
from bee.helper import SQLAlchemy

db = SQLAlchemy()

class Orders(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    type_id = db.Column(db.Integer)  
    type_id2 = db.Column(db.SMALLINT)
    name = db.Column(db.String(64), unique=True)  
    name2 = db.Column(db.String(), unique=True)  
    remark = db.Column(db.Text)  
    price = db.Column(db.Numeric(10, 2), nullable = False)  # 非空  
    price2 = db.Column(db.DECIMAL(10, 3), nullable = False)  # 非空  
    order_number = db.Column(db.BigInteger, unique = True)  # 唯一值  
    flage = db.Column(db.Boolean)
    
    field1 = db.Column(db.JSON)
    field2 = db.Column(db.Float)
    field3 = db.Column(db.SmallInteger)
    field4 = db.Column(db.REAL)
    
    field5 = db.Column(db.DateTime)
    field6 = db.Column(db.Date)
    field7 = db.Column(db.Time)
    
    def __repr__(self):  
        return  str(self.__dict__)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(16))
    tel = db.Column(db.String(16), unique=True)
    remark = db.Column(db.Text)
    
if __name__=='__main__':
    
    print("start")
    PreConfig.config_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\resources"
    
    try:
        db.create_all(True)
        db.create_one(Users,True)
    except Exception as e: 
            print(e)
            
    ## After generate the table, can generate the normal entity/bean with Assist in assist_api.py  
            
    print("end")
    
    # suidRich=SuidRich()
    # orders21=Orders21()
    # orders21.ID=1
    # orders21.Flage=1
    # # orders21.Name='abc'
    #
    # # print(orders21.__dict__)
    # # print(Orders21.__dict__)
    # # print(Orders21.__annotations__)
    #
    # orderList=suidRich.select(orders21)
    #
    # # order = Orders21()  
    # # setattr(order, 'TypeID', 123)  # 动态设置字段值
    # # print(order)  
    #
    # if orderList is not None:
    #     for one in orderList: 
    #         # setattr(one, 'TypeID', 123)  # 动态设置字段值  
    #         print(one)
    # else:
    #     print(" --no data!")
    
