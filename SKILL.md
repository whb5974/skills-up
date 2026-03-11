---
name: postgres-admin
description: PostgreSQL database administration and query execution. Connect to databases, run queries, analyze performance, and manage database objects.
---

# PostgreSQL Admin Skill

## Capabilities

- Connect to PostgreSQL databases
- Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Create and manage database objects (tables, indexes, views)
- Analyze query performance (EXPLAIN ANALYZE)
- Backup and restore operations
- User and permission management
- Schema inspection and documentation

## Tools Used

- `psycopg2` or `psycopg2-binary` - PostgreSQL adapter
- `pgcli` - Interactive CLI (optional)
- `psql` - PostgreSQL command line

## Installation

```bash
pip install psycopg2-binary
```

## Connection String Format

```
postgresql://user:password@host:port/database
```

## Usage

When the user asks to work with PostgreSQL:

1. Get connection details (host, port, database, user, password)
2. Establish connection
3. Execute queries safely
4. Return results in readable format
5. Handle errors gracefully

## Example Commands

```python
import psycopg2
from psycopg2.extras import RealDictCursor

# Connect
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="myuser",
    password="mypassword"
)

# Execute query
with conn.cursor(cursor_factory=RealDictCursor) as cur:
    cur.execute("SELECT * FROM users WHERE active = %s", (True,))
    results = cur.fetchall()
    for row in results:
        print(row)

# Explain query
cur.execute("EXPLAIN ANALYZE SELECT * FROM users")
print(cur.fetchall())

conn.close()
```

## Safety Rules

- NEVER execute DROP, TRUNCATE, or DELETE without confirmation
- ALWAYS use parameterized queries to prevent SQL injection
- Use transactions for multiple related operations
- Log all destructive operations

## Common Queries

```sql
-- List tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Table structure
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'your_table';

-- Indexes
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'your_table';

-- Row count
SELECT relname, n_live_tup FROM pg_stat_user_tables;
```

## Notes

- Always close connections after use
- Use connection pooling for multiple queries
- Handle timezone awareness properly
