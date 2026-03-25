import os

MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Admin1234')
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_DB = os.environ.get('MYSQL_DB', 'studygroup_db')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-key-change-this')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"