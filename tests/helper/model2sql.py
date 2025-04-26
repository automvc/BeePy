# from bee.api import SuidRich
# from bee.config import HoneyConfig

import MyConfig
from bee.helper import SQLAlchemy


# from bee.honeyfactory import BF
# 创建db实例  
db = SQLAlchemy()

class Orders2(db.Model):  
    ID = db.Column(db.Integer, primary_key=True)  
    TypeID = db.Column(db.Integer)  
    TypeID2 = db.Column(db.SMALLINT)
    Name = db.Column(db.String(64), unique=True)  
    Name2 = db.Column(db.String(), unique=True)  
    Remark = db.Column(db.Text)  
    PRICE = db.Column(db.Numeric(10, 2), nullable = False)  # 非空  
    PRICE2 = db.Column(db.DECIMAL(10, 3), nullable = False)  # 非空  
    ORDER_NUMBER = db.Column(db.BigInteger, unique = True)  # 唯一值  
    Flage = db.Column(db.Boolean)
    
    Field1 = db.Column(db.JSON)
    Field2 = db.Column(db.Float)
    Field3 = db.Column(db.SmallInteger)
    Field4 = db.Column(db.REAL)
    
    Field5 = db.Column(db.DateTime)
    Field6 = db.Column(db.Date)
    Field7 = db.Column(db.Time)
    
    def __repr__(self):  
        return  str(self.__dict__)

#
# 组织机构表
class Organization(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    TypeID = db.Column(db.Integer,nullable=False)
    Name = db.Column(db.String(64), unique=True)
    Remark = db.Column(db.Text)

# 用户表
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(16))
    tel = db.Column(db.String(16), unique=True)
    remark = db.Column(db.Text)

    
    
    
if __name__=='__main__':
    
    ######1. just print create table sql
    # honeyConfig = HoneyConfig()
    # # honeyConfig.set_dbname("MySQL")
    # # honeyConfig.set_dbname("Oracle")
    # # honeyConfig.set_dbname("sqlite")
    # honeyConfig.set_dbname("H2")
    #
    # # 调用create_all会打印模型结构信息  
    # # 
    # all_sql,_ = db.to_create_all_sql() 
    # for sql in all_sql:
    #     print(sql) 
    
    print("start")
    MyConfig.init()
    
    #######2. create all table
    db.create_all() 
    # db.create_all(True)
  
    
    try:
        db.create_one(Organization)
        # db.create_one(Organization, True)
        pass
    except Exception as e: 
            print(e)
            
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
    
