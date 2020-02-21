import itertools
import mysql.connector
from colorama import init
from colorama import Fore, Back, Style
from mysql.connector import Error
import masterenvironment as en
from os import system
from sys import argv
from os import chdir
from time import sleep
init()

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def readNodes():
    global lineList
    with open(en.fileName) as f:
        lineList = f.readlines()
    lineList = [line.rstrip('\n') for line in open(en.fileName)]

def db_connect():
    curr_node = 0
    curr_chunk = 0
    print("Connecting to DB ", end="")
    try:
        mydb = mysql.connector.connect(
            host=en.host, user=en.user, passwd=en.passwd, database=en.database)
        mycursor = mydb.cursor()
        print(Fore.GREEN+"[SUCCESS]"+Style.RESET_ALL)
        pending = []
        query = "select * from {} where PredictedOutcome {}".format("diagnosis", "IS NULL")
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        for x in myresult:
            pending.append(x[0])
        x = list(divide_chunks(pending, en.chunkSize))
        executeStatus = 0
        nodeCount = len(lineList)
        nodeCount = nodeCount - 1
        chunkCount = len(x)
        while(executeStatus != 1):
            if(len(x)==0):
                print("No Queries at the moment.")
                break
            temp = x[curr_chunk]
            temp = str(temp)
            temp = temp[1:-1]
            temp = temp.replace(" ", "")
            query = "ssh -o ConnectTimeout=10 pi@{} python3 hive-ml/slave.py {}".format(lineList[curr_node], temp)
            query = str(query)
            system(query)
            curr_chunk = curr_chunk + 1
            if(curr_node == nodeCount):
                curr_node = 0
            else:
                curr_node = curr_node+1
            if(curr_chunk == chunkCount):
                executeStatus = 1

    except Error as e:
        print(Fore.RED+"[FAILED]"+Style.RESET_ALL)
        print(e)
        exit(0)


if __name__ == "__main__":
    readNodes()
    if(len(argv) == 1):
        print("Usage Error")
        exit(0)

    elif(argv[1] == "masterupdate"):
        print("Updating from GitHub.")
        system("git checkout master&&git pull origin master")
        print("Close program and restart.")

    elif (argv[1] == "run"):
        time = input("Enter time: ")
        while True:
            db_connect()
            sleep(int(time))

    elif (argv[1] == "slaveupdate"):
        print("Updating All slave nodes.")
        for i in lineList:
            query = "ssh -o ConnectTimeout=10 pi@{} bash updateNodes.sh".format(
                lineList[curr_node])
            query = str(query)
            system(query)
    
    elif (argv[1] == "clustershutdown"):
        print("Shutting Down All slave nodes.")
        for i in lineList:
            query = "ssh -o ConnectTimeout=10 pi@{} sudo poweroff".format(lineList)
            query = str(query)
            system(query)
            
    else:
        print("Error")
        
