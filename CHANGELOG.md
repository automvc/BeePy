
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

