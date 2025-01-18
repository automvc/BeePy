
Bee
=========
ORM Bee(BeePy) with Python!  
Bee是基于Python的ORM工具;  
Bee是Python版的ORM工具(Java版的是Bee).  

## 功能日志
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
is_sql_key_word_upper放配置  
打印日志级别字符  
完善日志输出  
增加PreConfig，可以指定配置文件的位置  
完善异常  

### **V1.5**
1. 添加Version  
2. 调整naming  
