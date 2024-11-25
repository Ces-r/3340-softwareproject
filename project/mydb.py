import mysql.connector 

# Create data base connection with Django
dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'password',
)

# middleware
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE IF NOT  EXISTS 3340databaseProject")
print("Hello data base 3340dataProject")

