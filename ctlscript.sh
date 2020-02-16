#!/bin/bash
# add update nodes
# add shutdown nodes
# add backgound script to run nodes
# add script to clear db



clear
echo "Hive Controller V1.0"
echo "By Alexander Rodrigues, 2019"
echo \$ $$

if [[ $EUID -ne 0 ]]; then echo "This script must be run as root." exit 1 fi

while true; do
    trap '{ 
            printf "\nHey, you pressed Ctrl-C.  Time to quit.\n" ;exit 1;
          }' INT
    printf "-->"
    read -r command_user
    
    if [[ $command_user == "updatenodes" ]]; then
        echo "Calling Update Procedure"
        `python3 updateNodes.py`
    
    elif [[ $command_user == "runnodes" ]]; then
        printf 'Enter number of cycles:'
        read -r cycles
        printf 'Enter sleep duration:'
        read -r sleeptime

        for ((i = 0 ; i < $cycles ; i++)); do
            `python3 master.py; sleep $sleeptime` 
            echo "completed " `$i+1`  
        done
    fi


done