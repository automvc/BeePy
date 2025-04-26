Bee
=========
**ORM Bee** in Python!  

**Bee** in Python url:  
https://github.com/automvc/BeePy  

**Bee** in Java url:  
https://github.com/automvc/bee  

## [中文介绍](../../../BeePy/blob/master/README_CN.md)  
[点击链接可查看中文介绍](../../../BeePy/blob/master/README_CN.md)  

## Requirement  
#### Python 3.x(suggest 3.8.10+)   

## Feature & Function:  
### **V1.0**  
1.The framework uses a unified API to operate the database;  
2.Single table query, modification, addition, and deletion (SUID);  
3.Developers only need to focus on the use of the SUID API, which is an object-oriented approach to the framework;  
4.The entity class corresponding to the table can only use ordinary entity classes, without the need to add additional table structure information and framework related information;  
5.You can specify which database to use based on the configuration information.  
6.Support anti SQL injection;  
7.Support native SQL;  
8.The framework is responsible for managing the implementation logic of connections, transaction commit, rollback, etc;  
9.The encoding complexity C (n) of ORM is O (1).  

### **V1.1**
1. SQL keywords, supporting capitalization;  
2. Batch insert: Batch insert;  
3. Reuse the connection to improve efficiency;  
4. Add system definition exceptions  

### **V1.3**
is_sql_key_word_upper can set upper/lower in configure  
Print log level characters  
Improve log output  
Add PreConfig to specify the location of the configuration file  
Improve anomalies  

### **V1.5**
**1.5.2**  
1. add Version  
2. adjust naming  
(uploaded the stability function before)  

**1.5.4(2025·Valentine's Day·LTS)**  
3. adjust exception and select_paging
4. add PreparedSql support custom SQL  
5. update toUpdateSQL function  
6. select_by_id  
7. delete_by_id  
8. select_fun  
9. count  
10. exist  
11. create_table  
12. index_normal  
13. unique  

**1.6.0(2025·International Labour Day)**  
1. Optimize BeeSql  
2. enhance the code  
3. Add naming conversion support  
4. add interceptors  
5. can print execute min time  
   can config the print execute min time  
6. adjust select_by_id,delete_by_id
def select_by_id(self, entity_class, *ids)  
def delete_by_id(self, entity_class, *ids)  
7. Preconfig.config.path is used to set the path where the configuration file/SQLite database file is located  
8. Support complex where statement constructor Condition   
   e.g. name!='aaa',age>=10, like, between,group by,having,order,paging(start,size)  
9. Support Update Set to set the expression constructor Condition for updates  
10. Select query supports specifying the fields to be queried  
11. transform the Result of the query  
12. Convert the type of setting parameters  
13. support cache  
	support md5 for cache key  
14. transform bool result  
15. enhance config  
16. support python version 3.8.10+  
17. generate bean/entity file  
18. bean/entity mid type support  
19. cache entity field_and_type  
20. Object oriented approach, when creating a table, supports declaring fields with unique constraints in entities and fields that are not allowed to be empty:  
    __unique_key__={"name","type"}  
    __not_null_filels__={"name","type"}  

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
