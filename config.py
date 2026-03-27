import os

MYSQL_USER = os.environ.get('MYSQLUSER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', 'Admin1234')
MYSQL_HOST = os.environ.get('MYSQLHOST', 'localhost')
MYSQL_DB = os.environ.get('MYSQLDATABASE', 'studygroup_db')
MYSQL_PORT = int(os.environ.get('MYSQLPORT', 3306))
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-change-this')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"add .
