from bee.osql.mid import MidSQL

# 直接赋值创建别名
# 用于兼容第三方框架生成数据库表。
SQLAlchemy = MidSQL 
'''
Used to generate database tables compatible with third-party framework.

eg:
```python

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
    price = db.Column(db.Numeric(10, 2), nullable = False)  # not null  
    price2 = db.Column(db.DECIMAL(10, 3), nullable = False)  # not null 
    order_number = db.Column(db.BigInteger, unique = True)  #  not null 
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
    PreConfig.config_path="E:\\Project-name\\resources" #need to change
    
    try:
        db.create_all(True)
        db.create_one(Users,True)
    except Exception as e: 
            print(e)
            
            
## After generate the table, can generate the normal entity/bean with Assist in assist_api.py            
            
```            

'''  

