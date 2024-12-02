import mysql.connector 

# Create data base connection with Django
dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Yuanne04',
)

# middleware
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE 3340databaseTEST")
print("Hello data base 3340data")