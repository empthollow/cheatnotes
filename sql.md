# Managing MYSQL
## SQL commands
### Databases
#### List databases
```sql
SHOW DATABASES;	
#### Sswitch to database
```sql
USE [DBNAME]; 
```
#### List tables in database
```sql
SHOW TABLES; 
```
### Tables
#### List columns in table
```sql
SHOW COLUMNS;
```
### Show mysql users
```sql
SELECT [user], [host] FROM [mysql.user]; 
```
### Show mysql user permissions
```sql
SHOW GRANTS FOR '[USER]'@'%';
```

---

## MySQL Cli
### Log in using cli
```bash
mysql -h <host> -P <port> -u <user> -p # options -p is prompt for pw; --password=[PASS] for entering pw on cli
```