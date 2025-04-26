Bee
=========
**ORM Bee** in Python!  
Bee(BeePy)是Python版的ORM工具(还有Java版的).  

**Bee** in Python url:  
https://github.com/automvc/BeePy  

**Bee** in Java url:  
https://github.com/automvc/bee  

## 环境要求  
#### Python 3.x(建议3.8.10+)   

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
**1.5.2**  
1. 添加Version  
2. 调整naming  
(上传之前的稳定版本)  

**1.5.4(2025·元宵节·LTS版)**  
3. 调整exception和select_paging  
4. 添加PreparedSql支持自定义SQL方式操作DB  
5. 更新toUpdateSQL方法  
6. select_by_id  
7. delete_by_id  
8. select_fun  
9. count  
10. exist  
11. create_table  
12. index_normal  
13. unique  

### **V1.6**
**1.6.0(2025·劳动节)**  
1. 优化BeeSql  
2. 增强代码  
3. 增加命名转换支持  
4. 增加拦截器支持  
5. 记录sql执行时间  
   可配置当sql执行时间小于一定值时不打印  
6. 调整select_by_id,delete_by_id:  
def select_by_id(self, entity_class, *ids)  
def delete_by_id(self, entity_class, *ids)  
7. PreConfig.config_path用于设置配置文件/Sqlite数据库文件所在的路径  
8. 支持复杂的where语句构造器Condition  
   e.g. name!='aaa',age>=10, like, between,group by,having,order,paging(start,size)  
9. 支持Update Set设置更新的表达式构造器Condition  
10. select查询支持指定要查询的字段  
11. 处理查询的Result结果;  
12. 转换设置参数的类型  
13. 缓存支持  
	缓存key支持使用md5  
14. 查询结果bool类型结果转换  
15. config 完善  
16. 支持python版本：3.8.10+    
17. generate bean/entity file  
18. bean/entity中间类型支持  
19. 缓存实体field_and_type  
20. 面向对象方式，创建表时，支持在实体声明唯一约束的字段和不允许为空的字段:  
    __unique_key__={"name","type"}  
    __not_null_filels__={"name","type"} 
    

快速开始:
=========	
## 安装依赖包  
在命令行输入以下命令: 

```shell
pip install ormbee
```

**ORM Bee** pypi url:  
https://pypi.org/project/ormbee/

## 1. 配置db连接信息  
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
            'host': 'localhost',  # 数据库主机  
            'user': 'root',  # 替换为您的 MySQL 用户名  
            'password': '',  # 替换为您的 MySQL 密码  
            'database': 'bee',  # 替换为您的数据库名称  
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_db_config_dict(dict_config)

```

#### 1.3.set connection directly:  

```python
        config = {  
            # 'dbname':'MySQL',
            'host': 'localhost',  # 数据库主机  
            'user': 'root',  # 替换为您的 MySQL 用户名  
            'password': '',  # 替换为您的 MySQL 密码  
            'database': 'bee',  # 替换为您的数据库名称  
            'port':3306
        }
        
        honeyConfig= HoneyConfig()
        honeyConfig.set_dbname("MySQL")
        
        conn = pymysql.connect(**config)
        factory=BeeFactory()
        factory.set_connection(conn)
        
```

## 2. 使用Bee操作数据库  

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
    
    #SuidRich: insert_batch,select_first,updateBy
    #复杂的where过滤条件、group,having,order by,Update Set等可使用Condition;

```

## 3. 其它功能

```python
主要API在bee.api.py
Suid: simple API for Select/Update/Insert/Delete
SuidRich : select_paging, insert_batch, updateBy, select_first,select_by_id,
delete_by_id,select_fun,count,exist,create_table,index_normal,unique
PreparedSql: select, select_dict, modify, modify_dict

```