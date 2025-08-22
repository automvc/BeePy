

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
    unique_key = "__unique_key__"  # unique_key set
    not_null_filels = "__not_null_filels__"  # not null filels set

    dbModuleName = "dbModuleName"
    dbname = "dbname"

    upper = "upper"

    # move to PreConfig
    # configPropertiesFileName = "bee.properties"
    # configJsonFileName = "bee.json"


class KeyWork:
    key_work = [
        'select', 'from', 'where', 'group', 'by', 'having', 'order', 'by',
        'limit', 'offset', 'insert', 'into', 'values', 'update', 'set', 'delete', 'truncate', 'create', 'alter',
        'drop', 'rename', 'column', 'table', 'view', 'index', 'join', 'inner', 'join', 'left', 'join', 'right',
        'join', 'full', 'join', 'cross', 'join', 'union', 'union', 'all', 'intersect', 'except', 'minus', 'distinct',
        'count', 'sum', 'avg', 'min', 'max', 'and', 'or', 'not', 'in', 'between', 'like', 'is', 'null', 'not',
        'primary', 'key', 'foreign', 'key', 'unique', 'check', 'default', 'auto_increment', 'commit', 'rollback',
        'savepoint', 'begin', 'transaction', 'grant', 'revoke', 'deny', 'with', 'cascade', 'constraint',
        'varchar'
    ]

    # 1. MySQL
    mysql_keywords = [
        'add', 'all', 'alter', 'and', 'as', 'asc', 'between', 'by', 'case',
        'check', 'column', 'create', 'delete', 'desc', 'distinct', 'drop', 'else', 'exists', 'from', 'group',
        'having', 'in', 'index', 'insert', 'into', 'is', 'key', 'like', 'limit', 'not', 'null', 'or', 'order',
        'primary', 'select', 'set', 'table', 'then', 'union', 'unique', 'update', 'values', 'view', 'where',
        'collate', 'partition', 'fulltext', 'spatial', 'temporary', 'if', 'not', 'if', 'ignore', 'low_priority',
        'high_priority', 'dual', 'explain'
    ]
    # 2. Oracle
    oracle_keywords = [
        'access', 'add', 'all', 'alter', 'and', 'any', 'as', 'asc', 'audit',
        'between', 'by', 'char', 'check', 'cluster', 'column', 'comment', 'compress', 'connect', 'create', 'current',
        'date', 'decimal', 'default', 'delete', 'desc', 'distinct', 'drop', 'else', 'exclusive', 'exists', 'file',
        'float', 'for', 'from', 'grant', 'group', 'having', 'identified', 'immediate', 'in', 'increment', 'index',
        'initial', 'insert', 'integer', 'intersect', 'into', 'is', 'key', 'level', 'like', 'lock', 'long',
        'maxextents', 'minus', 'mlslabel', 'mode', 'modify', 'noaudit', 'nocompress', 'not', 'nowait', 'null',
        'number', 'of', 'off', 'offline', 'on', 'online', 'option', 'or', 'order', 'pctfree', 'prior', 'privileges',
        'public', 'raw', 'rename', 'resource', 'revoke', 'row', 'rowid', 'rownum', 'rows', 'select', 'session', 'set',
        'share', 'size', 'smallint', 'start', 'successful', 'synonym', 'sysdate', 'table', 'then', 'to', 'trigger',
        'uid', 'union', 'unique', 'update', 'user', 'validate', 'values', 'varchar', 'varchar2', 'view', 'whenever',
        'where', 'with'
    ]
    # 4. MariaDB
    mariadb_keywords = mysql_keywords

    # 5. H2
    h2_keywords = [
        'all', 'and', 'any', 'array', 'as', 'asymmetric', 'authorization',
        'between', 'both', 'case', 'cast', 'check', 'constraint', 'create', 'current_catalog', 'current_date',
        'current_path', 'current_role', 'current_schema', 'current_time', 'current_timestamp', 'current_user', 'day',
        'default', 'distinct', 'drop', 'else', 'end', 'except', 'exists', 'false', 'fetch', 'filter', 'for',
        'foreign', 'from', 'full', 'group', 'having', 'hour', 'if', 'in', 'inner', 'intersect', 'into', 'is', 'join',
        'leading', 'like', 'limit', 'localtime', 'localtimestamp', 'minus', 'minute', 'month', 'natural', 'not',
        'null', 'offset', 'on', 'or', 'order', 'outer', 'over', 'partition', 'primary', 'range', 'regexp', 'right',
        'row', 'rownum', 'second', 'select', 'session_user', 'set', 'some', 'symmetric', 'system_user', 'table', 'to',
        'trailing', 'true', 'union', 'unique', 'unknown', 'user', 'using', 'values', 'when', 'where', 'window',
        'with', 'year'
    ]
    # 6. SQLite
    sqlite_keywords = [
        'abort', 'action', 'add', 'after', 'all', 'alter', 'analyze', 'and',
        'as', 'asc', 'attach', 'autoincrement', 'before', 'begin', 'between', 'by', 'cascade', 'case', 'cast',
        'check', 'collate', 'column', 'commit', 'conflict', 'constraint', 'create', 'cross', 'current_date',
        'current_time', 'current_timestamp', 'database', 'default', 'deferrable', 'deferred', 'delete', 'desc',
        'detach', 'distinct', 'drop', 'each', 'else', 'end', 'escape', 'except', 'exclusive', 'exists', 'explain',
        'fail', 'for', 'foreign', 'from', 'full', 'glob', 'group', 'having', 'if', 'ignore', 'immediate', 'in',
        'index', 'indexed', 'initially', 'inner', 'insert', 'instead', 'intersect', 'into', 'is', 'isnull', 'join',
        'key', 'left', 'like', 'limit', 'match', 'natural', 'no', 'not', 'notnull', 'null', 'of', 'offset', 'on',
        'or', 'order', 'outer', 'plan', 'pragma', 'primary', 'query', 'raise', 'recursive', 'references', 'regexp',
        'reindex', 'release', 'rename', 'replace', 'restrict', 'right', 'rollback', 'row', 'savepoint', 'select',
        'set', 'table', 'temp', 'temporary', 'then', 'to', 'transaction', 'trigger', 'union', 'unique', 'update',
        'using', 'vacuum', 'values', 'view', 'virtual', 'when', 'where', 'with', 'without'
    ]

    # 7. PostgreSQL
    postgresql_keywords = [
        'all', 'analyse', 'analyze', 'and', 'any', 'array', 'as', 'asc',
        'asymmetric', 'authorization', 'between', 'binary', 'both', 'case', 'cast', 'check', 'collate', 'column',
        'concurrently', 'constraint', 'create', 'cross', 'current_catalog', 'current_date', 'current_role',
        'current_schema', 'current_time', 'current_timestamp', 'current_user', 'default', 'deferrable', 'desc',
        'distinct', 'do', 'else', 'end', 'except', 'false', 'fetch', 'for', 'foreign', 'from', 'full', 'grant',
        'group', 'having', 'in', 'initially', 'inner', 'intersect', 'into', 'is', 'isnull', 'join', 'lateral',
        'leading', 'left', 'like', 'limit', 'localtime', 'localtimestamp', 'not', 'notnull', 'null', 'offset', 'on',
        'only', 'or', 'order', 'outer', 'overlaps', 'placing', 'primary', 'references', 'returning', 'right',
        'select', 'session_user', 'similar', 'some', 'symmetric', 'table', 'then', 'to', 'trailing', 'true', 'union',
        'unique', 'user', 'using', 'variadic', 'when', 'where', 'window', 'with'
    ]

    # 8. MS Access
    msaccess_keywords = [
        'add', 'all', 'alphanumeric', 'alter', 'and', 'any', 'as', 'asc',
        'autoincrement', 'avg', 'between', 'binary', 'bit', 'boolean', 'by', 'byte', 'char', 'character', 'column',
        'compactdatabase', 'constraint', 'container', 'count', 'counter', 'create', 'createdatabase', 'createfield',
        'creategroup', 'createindex', 'createobject', 'createproperty', 'createtabledef', 'createuser',
        'createworkspace', 'currency', 'currentuser', 'database', 'date', 'datetime', 'delete', 'desc', 'disallow',
        'distinct', 'distinctrow', 'document', 'double', 'drop', 'echo', 'else', 'end', 'eqv', 'exists', 'exit',
        'false', 'field', 'fields', 'fillcache', 'float', 'float4', 'float8', 'foreign', 'form', 'forms', 'from',
        'full', 'function', 'general', 'getoption', 'getvalue', 'global', 'group', 'guid', 'having', 'idle',
        'ieeedouble', 'ieeesingle', 'ignore', 'imp', 'in', 'index', 'index', 'inner', 'insert', 'inserttext', 'int',
        'integer', 'integer1', 'integer2', 'integer4', 'into', 'is', 'join', 'key', 'left', 'level', 'like',
        'logical', 'logical1', 'long', 'longbinary', 'longtext', 'macro', 'match', 'max', 'min', 'mod', 'money',
        'move', 'name', 'newpassword', 'no', 'not', 'notnull', 'null', 'number', 'numeric', 'object', 'oleobject',
        'on', 'openrecordset', 'option', 'or', 'order', 'outer', 'owneraccess', 'parameter', 'parameters', 'partial',
        'percent', 'pivot', 'primary', 'procedure', 'property', 'queries', 'query', 'querydef', 'quit', 'real',
        'recalc', 'recordset', 'references', 'refresh', 'refreshlink', 'registerdatabase', 'relation', 'repaint',
        'replication', 'reports', 'requery', 'right', 'screen', 'section', 'select', 'set', 'setfocus', 'setoption',
        'short', 'single', 'smallint', 'some', 'sql', 'stdev', 'stdevp', 'string', 'sum', 'table', 'tabledef',
        'tabledefs', 'tableid', 'text', 'time', 'timestamp', 'top', 'transform', 'true', 'type', 'union', 'unique',
        'update', 'user', 'value', 'var', 'varp', 'varbinary', 'varchar', 'where', 'with', 'workspace', 'xor', 'year',
        'yes', 'yesno'
    ]

    # 9. 金仓 (Kingbase)
    kingbase_keywords = postgresql_keywords

    # 10. 达梦 (DM)
    dm_keywords = [
        'add', 'all', 'alter', 'and', 'any', 'as', 'asc', 'audit', 'between',
        'by', 'char', 'check', 'cluster', 'column', 'comment', 'compress', 'connect', 'create', 'current', 'date',
        'decimal', 'default', 'delete', 'desc', 'distinct', 'drop', 'else', 'exclusive', 'exists', 'file', 'float',
        'for', 'from', 'grant', 'group', 'having', 'identified', 'immediate', 'in', 'increment', 'index', 'initial',
        'insert', 'integer', 'intersect', 'into', 'is', 'key', 'level', 'like', 'lock', 'long', 'maxextents', 'minus',
        'mlslabel', 'mode', 'modify', 'noaudit', 'nocompress', 'not', 'nowait', 'null', 'number', 'of', 'off',
        'offline', 'on', 'online', 'option', 'or', 'order', 'pctfree', 'prior', 'privileges', 'public', 'raw',
        'rename', 'resource', 'revoke', 'row', 'rowid', 'rownum', 'rows', 'select', 'session', 'set', 'share', 'size',
        'smallint', 'start', 'successful', 'synonym', 'sysdate', 'table', 'then', 'to', 'trigger', 'uid', 'union',
        'unique', 'update', 'user', 'validate', 'values', 'varchar', 'varchar2', 'view', 'whenever', 'where',
        'with'
    ]

