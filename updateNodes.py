import masterenvironment as en
from os import system

with open(en.fileName) as f:
    lineList = f.readlines()
    
lineList = [line.rstrip('\n') for line in open(en.fileName)]

print("Updating All Nodes.")

for i in lineList:
    query = "ssh -o ConnectTimeout=10 pi@{} bash hive-ml/updateNodes.sh".format(lineList)
    query = str(query)
    system(query)

print("All nodes updated via Git.")