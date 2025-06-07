

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


class KeyWork:
    key_work = [
        'select', 'from', 'where', 'group', 'by', 'having', 'order', 'by', 'limit', 'offset',
        'insert', 'into', 'values', 'update', 'set', 'delete', 'truncate',
        'create', 'alter', 'drop', 'rename', 'table', 'view', 'index', 'sequence',
        'join', 'inner', 'join', 'left', 'join', 'right', 'join', 'full', 'join', 'cross', 'join',
        'union', 'union', 'all', 'intersect', 'except', 'minus',
        'distinct', 'count', 'sum', 'avg', 'min', 'max',
        'and', 'or', 'not', 'in', 'between', 'like', 'is', 'null', 'is', 'not', 'null',
        'primary', 'key', 'foreign', 'key', 'unique', 'check', 'default', 'auto_increment',
        'commit', 'rollback', 'savepoint', 'begin', 'transaction',
        'grant', 'revoke', 'deny', 'with', 'cascade', 'constraint'
    ]
    
    
    # 1. MySQL
    mysql_keywords = [
        'engine', 'auto_increment', 'charset', 'collate', 'storage', 'partition',
        'fulltext', 'spatial', 'temporary', 'if', 'not', 'exists', 'if', 'exists',
        'delayed', 'ignore', 'low_priority', 'high_priority', 'sql_cache', 'sql_no_cache'
    ]
    # 2. Oracle
    oracle_keywords = [
        'dual', 'rownum', 'rowid', 'nvl', 'nvl2', 'decode', 'connect', 'by',
        'start', 'with', 'prior', 'level', 'sysdate', 'systimestamp', 'sequence',
        'flashback', 'purge', 'within', 'group', 'over', 'partition', 'by', 'model'
    ]
    # 4. MariaDB
    mariadb_keywords = [
        'engine', 'auto_increment', 'charset', 'collate', 'storage', 'partition',
        'fulltext', 'spatial', 'temporary', 'if', 'not', 'exists', 'if', 'exists',
        'delayed', 'ignore', 'low_priority', 'high_priority', 'sql_cache', 'sql_no_cache'
    ]
    # 5. H2
    h2_keywords = [
        'cache', 'group_concat', 'merge', 'offset', 'rownum', 'top', 'truncate', 'value'
    ]
    # 6. SQLite
    sqlite_keywords = [
        'autoincrement', 'conflict', 'fail', 'ignore', 'replace', 'rollback', 'abort',
        'without', 'rowid', 'vacuum', 'attach', 'detach', 'temp', 'temporary'
    ]
    # 7. PostgreSQL
    postgresql_keywords = [
        'ilike', 'similar', 'to', 'distinct', 'on', 'returning', 'serial', 'bigserial',
        'smallserial', 'with', 'oids', 'inherits', 'like', 'including', 'excluding',
        'with', 'time', 'zone', 'without', 'time', 'zone'
    ]
    # 8. MS Access
    msaccess_keywords = [
        'top', 'distinctrow', 'transform', 'pivot', 'param', 'declare', 'database',
        'workspace', 'dbengine', 'currentdb', 'currentuser', 'currentproject'
    ]
    # 9. 金仓 (Kingbase)
    kingbase_keywords = [
        'with', 'oids', 'inherits', 'like', 'including', 'excluding', 'serial',
        'bigserial', 'smallserial', 'returning', 'ilike', 'similar', 'to'
    ]
    # 10. 达梦 (DM)
    dm_keywords = [
        'dual', 'rownum', 'rowid', 'nvl', 'nvl2', 'decode', 'connect', 'by',
        'start', 'with', 'prior', 'level', 'sysdate', 'systimestamp', 'sequence'
    ]
    # 11. OceanBase
    oceanbase_keywords = [
        'dual', 'rownum', 'rowid', 'nvl', 'nvl2', 'decode', 'connect', 'by',
        'start', 'with', 'prior', 'level', 'sysdate', 'systimestamp', 'sequence'
    ]
    
    