import pymysql

# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# Fix version issue - tell Django we have a compatible version
pymysql.version_info = (2, 2, 1, "final", 0)