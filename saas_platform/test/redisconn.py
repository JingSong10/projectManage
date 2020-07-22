import redis
pool = redis.ConnectionPool(host="49.235.190.157", port=6379,password="p@ssw0rd0",max_connections=1024)
conn = redis.Redis(connection_pool=pool)
conn.set('username', "zhangsan")
print(conn.get("username"))