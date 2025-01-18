Bee
=========
ORM **Bee** with Python!  
Bee(BeePy)是Python版的ORM工具(还有Java版的).  

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

### **V1.1**
1. SQL 关键字，支持大小写；  
2. batch insert 批量插入；  
3. reuse the connection 重用 connection 连接，提高效率；  
4. 添加系统定义异常.  

### **V1.3**
1. is_sql_key_word_upper放配置  
2. 打印日志级别字符  
3. 完善日志输出  
4. 增加PreConfig，可以指定配置文件的位置  
5. 完善异常  
6. selectFirst  

### **V1.5**
1. 添加Version  

快速开始:
=========	
## 安装依赖包  
在命令行输入以下命令: 

```shell
pip install bee
```

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

## 2. 使用Bee操作数据库  

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
