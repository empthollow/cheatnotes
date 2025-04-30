### sql commands ###
SHOW DATABASES;	# list databases
USE [DBNAME]; # swiitch to database
SHOW TABLES; # list tables in databas
SELECT user, host FROM mysql.user; # show users
SHOW GRANTS FOR '[USER]'@'%';

### mysql cli ###
mysql -h <host> -P <port> -u <user> -p # options -p is prompt for pw; --password=[PASS] for entering pw on cli


