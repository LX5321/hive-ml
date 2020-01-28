import itertools
import mysql.connector
from colorama import init
from colorama import Fore, Back, Style
from mysql.connector import Error
import env_vars as en
init()

fileName = "config/hosts.txt"
name = []

# divide the query data into chunk of arrays
# to be processed as command line arguments


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def readNodes():
    # create a global linelist object
    global lineList
    with open(fileName) as f:
        lineList = f.readlines()
    lineList = [line.rstrip('\n') for line in open(fileName)]


def db_connect():
    # mycursor to use with queries outside the function.
    # keeps code small by enabling only queries to be run using one db connection object.
    global mycursor
    print("Connecting to DB ", end="")
    try:
        mydb = mysql.connector.connect(
            host=en.host, user=en.user, passwd=en.passwd, database=en.database)
        mycursor = mydb.cursor()
        print(Fore.GREEN+"[SUCCESS]"+Style.RESET_ALL)

    except Error as e:
        print(Fore.RED+"[FAILED]"+Style.RESET_ALL)
        print(e)
        exit(0)


def nodeControl():
    global executeStatus
    executeStatus = 0
    nodeCounts = 0
    query = "select * from {} where run={}".format("diagnosis", "0")
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for x in myresult:
            name.append(x[0])

        x = list(divide_chunks(name, en.chunkSize))

        while(executeStatus != 1):
            i = i+1
            lineList



if __name__ == "__main__":
    readNodes()
    db_connect()
