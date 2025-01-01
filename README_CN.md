# BeePy

## 简介
ORM Bee with Python!  
BeePy是基于Python的ORM工具;  
BeePy是Python版的ORM工具(Java版的是Bee).  

## 环境要求  
#### Python 3.x(建议3.12+)   

## 主要功能
### **V1.0**
1.框架使用统一的API操作DB；  
2.单表查改增删(SUID)；   
3.开发人员只需关注框架的面向对象方式SUID API的使用即可；  
4.表对应的实体类，可以只使用普通的实体类，不需要添加额外的表结构信息和框架相关信息；  
5.可以根据配置信息，指定使用哪种数据库。  
6.支持防sql注入；  
7.支持原生sql；  
8.框架负责管理连接，事务提交、回滚等的实现逻辑；  
9.ORM的编码复杂度C(n)是O(1)。

快速开始:
=========	
## 1. 配置db连接信息  
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
            'host': 'localhost',  # 数据库主机  
            'user': 'root',  # 替换为您的 MySQL 用户名  
            'password': '',  # 替换为您的 MySQL 密码  
            'database': 'bee',  # 替换为您的数据库名称  
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_dbName("MySQL")
        
        conn = pymysql.connect(**config)
        factory=BeeFactory()
        factory.setConnection(conn)
        
```

## 2. 使用BeePy操作数据库  

```python

	   # select record
        suid=Suid()
        orderList=suid.select(Orders())
        
```
