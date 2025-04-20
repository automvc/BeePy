

class DatabaseConst:
    MYSQL = "MySQL"
    MariaDB = "MariaDB"
    ORACLE = "Oracle"
    SQLSERVER = "Microsoft SQL Server"
    MsAccess = "Microsoft Access"  # Microsoft Access
    AzureSQL = SQLSERVER

    H2 = "H2"
    SQLite = "SQLite"
    PostgreSQL = "PostgreSQL"

    Cubrid = "Cubrid"
    DB2400 = "DB2 UDB for AS/400"
    DB2 = "DB2" 
    Derby = "Apache Derby"
    Firebird = "Firebird"
    FrontBase = "FrontBase"

    HSQL = "HSQL Database Engine"
    HSQLDB = "HSQL Database"
    Informix = "Informix Dynamic Server"
    Ingres = "Ingres"
    JDataStore = "JDataStore"
    Mckoi = "Mckoi"
    MimerSQL = "MimerSQL"
    Pointbase = "Pointbase"

    SAPDB = "SAPDB"
    Sybase = "Sybase SQL Server"
    Teradata = "Teradata"
    TimesTen = "TimesTen"

    DM = "DM DBMS"
    Kingbase = "KingbaseES"
    GaussDB = "GaussDB"

    OceanBase = "OceanBase"

    # NoSql
    Cassandra = "Cassandra"
    Hbase = "Hbase"
    Hypertable = "Hypertable"
    DynamoDB = "DynamoDB"

    MongoDB = "MongoDB"
    CouchDB = "CouchDB"

    
class StrConst:
    LOG_PREFIX = "[Bee]========"
    LOG_SQL_PREFIX = "[Bee] sql>>> "


class SysConst:
    tablename = "__tablename__"
    pk = "__pk__"
    primary_key = "__primary_key__"
    id = "id"
    unique_key="__unique_key__" # unique_key set
    not_null_filels="__not_null_filels__" # not null filels set
    
    dbModuleName = "dbModuleName"
    dbname = "dbname"
    
    upper = "upper"
    
    # move to PreConfig
    # configPropertiesFileName = "bee.properties"
    # configJsonFileName = "bee.json"
    
