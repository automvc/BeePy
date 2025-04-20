
Bee
=========
ORM Bee(BeePy) with Python!  

## Function Log:  
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

**1.6.0(2025)**  
1. 优化BeeSql  
2. 增强代码  
3. 增加命名转换支持  
4. 增加拦截器支持  
5. 记录sql执行时间  
6. 调用select_by_id,delete_by_id:  
def select_by_id(self, entity_class, *ids)  
def delete_by_id(self, entity_class, *ids)  
7. PreConfig.config_path用于设置配置文件/Sqlite数据库文件所在的路径  
8. 支持复杂的where语句构造器Condition  
   e.g. name!='aaa',age>=10, like, between,group by,having,order,paging(start,size)  
9. 支持Update Set设置更新的表达式构造器Condition  
10. select查询支持指定要查询的字段  
11. 处理查询的ResultSet结果;  
12. 转换设置参数的类型  
13. support cache  
	support md5 for cache key  
14. transform bool result  
15. config 完善；  
16. 可配置当sql执行时间小于一定值时不打印  
17. generate bean/entity file  
18. bean/entity mid type support  



