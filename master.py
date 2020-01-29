import itertools
import mysql.connector
from colorama import init
from colorama import Fore, Back, Style
from mysql.connector import Error
import env_vars as en
from os import system
init()


# divide the query data into chunk of arrays
# to be processed as command line arguments
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def readNodes():
    # create a global linelist object
    global lineList
    with open(en.fileName) as f:
        lineList = f.readlines()
    lineList = [line.rstrip('\n') for line in open(en.fileName)]


def db_connect():
    # mycursor to use with queries outside the function.
    # keeps code small by enabling only queries to be run using one db connection object.
    # global mycursor
    curr_node = 0
    curr_chunk = 0
    print("Connecting to DB ", end="")
    try:
        mydb = mysql.connector.connect(
            host=en.host, user=en.user, passwd=en.passwd, database=en.database)
        mycursor = mydb.cursor()
        print(Fore.GREEN+"[SUCCESS]"+Style.RESET_ALL)
        pending = []
        query = "select * from {} where run={}".format("diagnosis", "0")
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        for x in myresult:
            pending.append(x[0])

        x = list(divide_chunks(pending, en.chunkSize))
        # checks if all the queries are complete.
        # executeStatus == 0 -> queries are not complete.
        # executeStatus == 1 -> complete, exit loop.
        executeStatus = 0
        # number of nodes
        nodeCount = len(lineList)
        # since array starts from 0 - n
        nodeCount = nodeCount - 1
        # number of chunks
        chunkCount = len(x)
        while(executeStatus != 1):
            temp = x[curr_chunk]
            temp = str(temp)
            temp = temp[1:-1]
            temp = temp.replace(" ", "")
            # print(temp)
            query = "python3 slave.py {} {}".format(temp, lineList[curr_node])
            query = str(query)
            # ssh user@host python -u - --opt arg1 arg2 < script.py
            system(query)

            # update the current chunk to the next chunk.
            curr_chunk = curr_chunk + 1
            # update the hostlist counter
            if(curr_node == nodeCount):
                curr_node = 0
            else:
                curr_node = curr_node+1
            # stop the loop by updating the flag
            if(curr_chunk == chunkCount):
                executeStatus = 1

    except Error as e:
        print(Fore.RED+"[FAILED]"+Style.RESET_ALL)
        print(e)
        exit(0)

if __name__ == "__main__":
    readNodes()
    db_connect()
