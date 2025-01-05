BeePy
=========
ORM Bee with Python!  
BeePy is a Python based ORM tool;  
BeePy is a Python version of ORM tool (the Java version is Bee)  

## Requirement  
#### Python 3.x(suggest 3.12+)   

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

Quick Start:
=========	
## 1. set db config  
#### 1.1.can custom your db Module  
in bee.json or bee.properties set dbModuleName  
#### 1.2.if do not want to use the default config file(bee.json or bee.properties),  
can set the db_config info yourself.  

```python
        # #mysql
        config = {  
            'dbName':'MySQL',
            'host': 'localhost',  # 数据库主机  
            'user': 'root',  # 替换为您的 MySQL 用户名  
            'password': '',  # 替换为您的 MySQL 密码  
            'database': 'bee',  # 替换为您的数据库名称  
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_db_config_dict(config)

```

#### 1.3.set connection directly:  

```python
        config = {  
            # 'dbName':'MySQL',
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'bee',
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_dbName("MySQL")
        
        conn = pymysql.connect(**config)
        factory=BeeFactory()
        factory.setConnection(conn)
        
```

## 2. operate DB  

```python

    # select record
    suid=Suid()
    orderList=suid.select(Orders()) #select all
    
    #insert    
    orders=Orders()
    orders.id=104
    orders.name="bee"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    #update/delete
    orders=Orders3()
    orders.name="bee130"
    orders.ext="aaa"  #实体没有字段，会被忽略。出去安全考虑
    orders.id=10002
    
    suid = Suid()
    n1= suid.update(orders)
    n2= suid.delete(orders)
    print(n1)
    print(n2)
    
    #batch insert
    student0=Student2()
    student0.name = "bee"
    student1=Student2()
    student1.name = "bee1"
    student1.addr=""
    student1.age=40
    entity_list=[]
    entity_list.append(student0)
    entity_list.append(student1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)

```



