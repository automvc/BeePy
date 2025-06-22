"""   
### **V1.6.2**  
**ORM Bee** in Python!  

**Bee** in Python url:  
https://github.com/automvc/BeePy  

**Bee** in Java url:  
https://github.com/automvc/bee  


Quick Start:
=========    
## Installation  
To install, type: 

```shell
pip install ormbee
```
**ORM Bee** pypi url:  
https://pypi.org/project/ormbee/

## 1. set db config  
#### 1.1.can custom your db Module  
in bee.json or bee.properties set dbModuleName  

```json
 {
 "dbname": "SQLite",  
 "database": "bee.db", 
 //default support: pymysql,sqlite3,cx_Oracle,psycopg2 (no need set)
 "dbModuleName":"sqlite3"
 }
 ```
 
 ```properties
 #value is: MySql,SQLite,Oracle,
#MySQL config
#bee.db.dbname=MySQL
#bee.db.host =localhost
#bee.db.user =root
#bee.db.password =
#bee.db.database =bee
#bee.db.port=3306

# SQLite
bee.db.dbname=SQLite
bee.db.database =bee.db
 ```
 
#### 1.2.if do not want to use the default config file(bee.json or bee.properties),  
can set the db_config info yourself.  

```python
        # #mysql
        dict_config = {  
            'dbname':'MySQL',
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'bee',
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_db_config_dict(dict_config)

```

#### 1.3.set connection directly:  

```python
        config = {  
            # 'dbname':'MySQL',
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'bee',
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_dbname("MySQL")
        
        conn = pymysql.connect(**config)
        factory=BeeFactory()
        factory.set_connection(conn)
        
```

## 2. operate DB with Bee

```python

class Orders:
    id = None  
    name = None 
    remark = None

    # can ignore
    def __repr__(self): 
        return  str(self.__dict__)

  
# also can use field type as :int        
class Orders8:
    __tablename__ = "orders"
    id:int = None  
    name:str = None 
    remark:str = None

    def __repr__(self): 
        return  str(self.__dict__)

        
class Student2:
    id = None
    name = None 
    age = None  
    remark = None
    addr = None

    def __repr__(self): 
        return  str(self.__dict__)
        
        
from bee.api import Suid, SuidRich
from bee.config import PreConfig
from bee.honeyfactory import BF
from bee.osql.bee_enum import Op

if __name__ == "__main__":

    # set bee.properties/bee.json config folder
    PreConfig.config_path="E:\\Bee-Project\\resources"

    # select record
    suid = Suid()
    orderList = suid.select(Orders())  # select all
    
    # insert    
    orders = Orders()
    orders.id = 1
    orders.name = "bee"
    orders.remark = "test"
    
    suid = Suid()
    suid.insert(orders)
    
    # update/delete
    orders = Orders()
    orders.name = "bee130"
    # For safety reasons
    # Fields that are not present in the entity will be ignored.
    orders.ext = "aaa"  
    orders.id = 1
    
    suid = Suid()
    n1 = suid.update(orders)
    n2 = suid.delete(orders)
    print(n1)
    print(n2)
    
    # batch insert
    student0 = Student2()
    student0.name = "bee"
    student1 = Student2()
    student1.name = "bee1"
    student1.addr = ""
    student1.age = 40
    entity_list = []
    entity_list.append(student0)
    entity_list.append(student1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    #how to use Condition for advanced query and update
    condition = BF.condition()
    condition.op("age", Op.ge, 22)
    condition.op("remark", Op.eq, None)
    stuList = suidRich.select(Student2(), condition)
    # select ... from student2 where age >= ? and remark is null
    for stu in stuList:
        print(stu)
    
    # all stu'age add 1 if id>5
    condition = BF.condition()
    condition.setAdd("age", 1)
    condition.op("id", Op.ge, 5)
    updateNum = suidRich.updateBy(Student2(), condition)
    # update student2 set age = age + ? where id >= ?
    print("updateNum:", updateNum)
    
    # SuidRich: insert_batch,select_first,updateBy
    # complex where statement constructor Condition

```

## 3. Others

```python
Main API in bee.api.py
Suid: simple API for Select/Update/Insert/Delete
SuidRich : select_paging, insert_batch, updateBy, select_first,select_by_id,
delete_by_id,select_fun,count,exist,create_table,index_normal,unique
PreparedSql: select, select_dict, modify, modify_dict

```


 
Corresponding Java type ORM tool,
JAVA ORM Bee:

       maven:
       <dependency>
          <groupId>org.teasoft</groupId>
          <artifactId>bee-all</artifactId>
          <version>2.4.2</version>
        </dependency>
        
        Gradle(Short):
        implementation 'org.teasoft:bee-all:2.4.2'
        
        note:the version can change to newest.

"""
from bee.version import Version

Version.printversion()
