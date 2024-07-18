import os

DB_USER = os.getenv('MYSQL_USER', 'libuser')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('MYSQL_DATABASE', 'library_db')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()
