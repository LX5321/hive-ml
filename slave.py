#!/usr/bin/env python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sys import argv as a
from time import sleep as s
import env_vars as en
import itertools
import mysql.connector

temp = (a[1])
temp = temp.split(',')

try:
    mydb = mysql.connector.connect(host=en.host, user=en.user, passwd=en.passwd, database=en.database)
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

        
diabetes = pd.read_csv('diabetes.csv')
X_train, X_test, y_train, y_test = train_test_split(diabetes.loc[:, diabetes.columns != 'Outcome'], diabetes['Outcome'], stratify=diabetes['Outcome'], random_state=66)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

mlp = MLPClassifier(random_state=42)
mlp.fit(X_train_scaled, y_train)

print("Accuracy on training set: {:.3f}".format(mlp.score(X_train_scaled, y_train)))
print("Accuracy on test set: {:.3f}".format(mlp.score(X_test_scaled, y_test)))

sol = (mlp.predict([[3,185,36,239,1,236.6,0.701,31]]))
sol = float(sol)
print(sol)
   

if __name__ == "__main__":
    for queries in temp:
	    db_connect(queries)
