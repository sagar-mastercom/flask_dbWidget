from flask import request
from flask_smorest import Blueprint
import mysql.connector



databases_bp = Blueprint("databases",__name__,description="Operations on Database")

# config = {
#   'user': 'root',
#   'password': 'tiger',
#   'host': 'localhost',
#   'raise_on_warnings': True
# }


# cnx = mysql.connector.connect(**config)


class DBManager:
    def __init__(self,config):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def get_databaseNames(self):
        
        self.cursor.execute('SHOW DATABASES')
        dbNames = [db[0] for db in self.cursor]
        print(dbNames)
        return dbNames
      
          
    
    def get_tableNames(self,dbName):
      self.cursor.execute(f'use {dbName}')
      self.cursor.execute('SHOW TABLES')
      tableNames = [table[0] for table in self.cursor]
      print(tableNames)
      #self.cnx.close()
      return tableNames
      
        
    def get_columnNames(self,dbName,tableName):
        #self.cursor.execute(f'use {dbName}')
        self.cursor.execute(f"DESC {dbName}.{tableName}")
        columnNames = [column[0] for column in self.cursor]
        print(columnNames)
        #self.cnx.close()
        return columnNames
        

    def get_data(self,dbName,query):
      self.cursor.execute(f'use {dbName}')
      self.cursor.execute(query)
      data = self.cursor.fetchall()
      print(data)
      #self.cnx.close()
      return data


conn = None

@databases_bp.route('/connect',methods=['post','get'])
def connect_db():
    request_data =request.get_json()
    global conn
    # if conn is None:
    #     print("Connecting to database..............")
    #     conn = DBManager(request_data["config"])
    
    conn = DBManager(request_data['config'])
    print("*"*20)
    if (conn.cnx.is_connected()):
      print("Connected")
      print(conn.cnx.is_connected())
    else:
      print("Not connected")
      print(conn.cnx.is_connected())
    print("*"*20)
    dbNames = conn.get_databaseNames()
    conn.cursor.close()
    conn.cnx.close()
    return dbNames

@databases_bp.route('/gettablenames',methods=['post','get'])
def getDbNames():
    global conn
    request_data =request.get_json()
    # if conn is None:
    #     print("Connecting to database..............")
    #     conn = DBManager(request_data['config'])
    
    conn = DBManager(request_data['config'])
    print("*"*20)
    if (conn.cnx.is_connected()):
      print("Connected")
      print(conn.cnx.is_connected())
    else:
      print("Not connected")
      print(conn.cnx.is_connected())
    print("*"*20)
    tables = conn.get_tableNames(request_data['dbName'])
    conn.cursor.close()
    conn.cnx.close()
    return tables

@databases_bp.route('/gettabledata',methods=['post','get'])
def get_tableData():
    global conn
    request_data =request.get_json()
    # if conn is None:
    #     print("Connecting to database..............")
    #     conn = DBManager(request_data['config'])

    conn = DBManager(request_data['config'])
    print("*"*20)
    if (conn.cnx.is_connected()):
      print("Connected")
      print(conn.cnx.is_connected())
    else:
      print("Not connected")
      print(conn.cnx.is_connected())
    print("*"*20)

    selected_columns = "*"
    if len(request_data["selectedColumns"]) > 0:
       selected_columns = ", ".join(request_data["selectedColumns"])


    data = conn.get_data(request_data["dbName"],f"SELECT {selected_columns} FROM {request_data['tableName']}")
    conn.cursor.close()
    conn.cnx.close()
    return data
    
@databases_bp.route('/getcolumnnames',methods=['post','get'])
def getColumnNames():
    global conn
    
    request_data =request.get_json()
    # if conn is None:
    #     print("Connecting to database..............")
    #     conn = DBManager(request_data['config'])

    conn = DBManager(request_data['config'])
    print("*"*20)
    if (conn.cnx.is_connected()):
      print("Connected")
      print(conn.cnx.is_connected())
    else:
      print("Not connected")
      print(conn.cnx.is_connected())
    print("*"*20)

    columnNames = conn.get_columnNames(request_data["dbName"],request_data["tableName"])
    conn.cursor.close()
    conn.cnx.close()
    return columnNames