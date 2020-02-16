#!/bin/bash
# add update nodes

clear
echo "Hive Controller V1.0"
echo "By Alexander Rodrigues, 2019"
echo \$ $$

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

while true; do
    trap '{ 
            printf "Hey, you pressed Ctrl-C.  Time to quit.\n" ;exit 1;
          }' INT
    printf 'Enter [y/n] : '
    read -r command_user
    `bash stay.sh $command_user >> log`
    echo "Hello" $command_user
done