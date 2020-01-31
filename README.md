# hive-ml
Script to access and run ML algorithms across multiple nodes with a master.

Assume a setup of a single master and multiple slave nodes across a system connected to the same database and same network.

## MASTER
Configure a master and run the script from the master folder which has the data stored in the ```.json``` file.

## SLAVE
The slave will access the database via the nodes sent in the command line arguments.
