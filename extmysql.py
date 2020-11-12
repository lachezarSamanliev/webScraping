import mysql.connector
#from mysql.connector import (connection)
#cnx = mysql.connector.connect(
#    host='localhost',
#    user='root',
#    password='0033lgBushdidit'
#)
#cur = cnx.cursor()
#cnx.close()
class db_helper:
    def __init__(self):
        #self.db = "upvotes_db"
        self.mydb = mysql.connector.connect(
            user='firesyst_lacho',
            password='RS.Firesystems-bg.SQL!',
            host='lima.rdb.superhosting.bg',
            database='firesyst_rs'
            )
        self.cursor = self.mydb.cursor(buffered=True)
        #if (mysql):
        #    print("good")
        #else:
        #    print("nope")

    def __disconnect__(self):
        self.cursor.close()
        self.mydb.close()
        #self.conn.close()

    def execute(self, sql_command, sql_values):
    #def execute(self, sql_command):
        self.__init__()
        self.cursor.execute(sql_command, sql_values)
        #self.cursor.execute(sql_command)
        #commit command saves the changes
        self.mydb.commit()
        self.__disconnect__()

    def executee(self, sql_command):
    #def execute(self, sql_command):
        self.__init__()
        #cursor = self.cursor(buffered=True)
        self.cursor.execute(sql_command)
        #self.cursor.execute(sql_command)
        #commit command saves the changes
        #self.mydb.commit()
        result = self.cursor.fetchall()
        self.__disconnect__()
        return result


        self.__disconnect__()


# query = "CREATE TABLE icons (id INT AUTO_INCREMENT PRIMARY KEY, icon_name VARCHAR(20) UNIQUE NOT NULL)"
# query_two = "SELECT * FROM razreshitelni"

#id_user (auto), email, password, date(auto), is_admin(auto)

#####DB ONE
# query_three = "INSERT INTO razreshitelni (date, province, project, investor, link_page) VALUES (%s, %s, %s, %s, %s)"
# data = ('13.05.2020', 'Варна', 'сграда ОД', 'банки', 'reddit.com')
#sem = db_helper()
#query = "SELECT * FROM accounts"
#sho =  sem.executee(query)
#print(sho)
# #sto = sem.executee(query_two)
# #print(sto)
# sem.execute(query_three, data)
#mycursor.execute("CREATE DATABASE testing")

#add_post = ("INSERT INTO employees "
             #  "(first_name, last_name, hire_date, gender, birth_date) "
             #  "VALUES (%s, %s, %s, %s, %s)")
#data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

#cursor.execute(add_post, data_employee)


# Make sure data is committed to the database
#cnx.commit()
#cursor.close()
#cnx.close()





#get posts from bots comments
#put in db


#translate
