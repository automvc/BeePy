
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

