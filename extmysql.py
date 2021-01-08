import mysql.connector

class db_helper:
    def __init__(self):
        #self.db = "upvotes_db"
        self.mydb = mysql.connector.connect(
            user='########',
            password='########',
            host='########',
            database='########'
            )
        self.cursor = self.mydb.cursor(buffered=True)


    def __disconnect__(self):
        self.cursor.close()
        self.mydb.close()
        #self.conn.close()

    def execute(self, sql_command, sql_values):
        self.__init__()
        self.cursor.execute(sql_command, sql_values)
        #commit command saves the changes
        self.mydb.commit()
        self.__disconnect__()

    def executee(self, sql_command):
        self.__init__()
        self.cursor.execute(sql_command)
        result = self.cursor.fetchall()
        self.__disconnect__()
        return result

        self.__disconnect__()

