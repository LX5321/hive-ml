from sys import argv as a
from time import sleep as s
import env_vars as en
import itertools
import mysql.connector
temp = (a[1])
temp = temp.split(',')


try:
    mydb = mysql.connector.connect(
        host=en.host, user=en.user, passwd=en.passwd, database=en.database)
    mycursor = mydb.cursor()
except Error as e:
        print(e)
        exit(0)

def db_connect(query_id):
        pending = []
        query = "select * from {} where id={}".format("diagnosis", query_id)
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)


   

if __name__ == "__main__":
    for queries in temp:
	    db_connect(queries)
