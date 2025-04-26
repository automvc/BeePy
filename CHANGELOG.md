
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

**1.6.0(2025·International Labour Day)**  
1. Optimize BeeSql  
2. enhance the code  
3. Add naming conversion support  
4. Add support for interceptors  
5. can print execute min time  
   can config the print execute min time  
6. select_by_id,delete_by_id:  
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

