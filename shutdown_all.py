import masterenvironment as en
from os import system

with open(en.fileName) as f:
    lineList = f.readlines()
    
lineList = [line.rstrip('\n') for line in open(en.fileName)]

print("Shutting Down All Nodes.")

for i in lineList:
    query = "ssh -o ConnectTimeout=10 pi@{} sudo poweroff".format(lineList)
    query = str(query)
    system(query)