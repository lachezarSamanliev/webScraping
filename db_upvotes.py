#Database access class
import sqlite3

class db_helper:

    def __init__(self):
        self.db = "razreshitelni"

    def __connect__(self):
        self.conn = conn = sqlite3.connect('razreshitelni')
        self.c = conn.cursor()

    def __disconnect__(self):
        self.conn.close()

    def fetch(self, command_choice):
        #I was going to pass int here so that I can choose which sql command to be executed
        #but it kept passing as a string and not SQL command
#        switcher = {
#            0: "SELECT * FROM upvotes_db",
#            1: "SELECT post_id FROM upvotes_db",
#            2: ""SELECT subreddit FROM upvotes_db"",
#            3: "SELECT title FROM upvotes_db",
#            4: "SELECT flag FROM upvotes_db",
#            5: "SELECT user FROM upvotes_db",
#            6: "SELECT upvotes FROM upvotes_db",
#            }
#        return switcher.get(command_choice, "ops")
        self.__connect__()
        self.c.execute(command_choice)
        result = self.c.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.c.execute(sql)
        #commit command saves the changes
        self.conn.commit()
        self.__disconnect__()

    def make_table(self):
        query = ("""CREATE TABLE IF NOT EXISTS razreshitelni (
                obshtina TEXT NOT NULL,
                date TEXT NOT NULL,
                tip_obekt TEXT NOT NULL,
                izpulnitel TEXT NOT NULL,
                UNIQUE(tip_obekt)
                )""")
        d = db_helper()
        d.execute(query)


#hp = db_helper()
#hp.make_table()
