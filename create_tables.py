import pymysql

conn = pymysql.connect(
    host='mysql://root:JqMtpoUVfaPRrzBEmwafcQhBYIocMxzx@hopper.proxy.rlwy.net:19754/railway',
    user='root',
    password='JqMtpoUVfaPRrzBEmwafcQhBYIocMxzx',
    database='railway',
    port=3306

)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    level VARCHAR(20)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS groups_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    course VARCHAR(100),
    description TEXT,
    max_members INT DEFAULT 10,
    schedule VARCHAR(100),
    location VARCHAR(200),
    creator_id INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS memberships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    group_id INT
)""")

conn.commit()
print("Tables created!")
conn.close()