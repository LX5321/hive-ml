#!/usr/bin/env python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sys import argv as a
import slaveenvironment as en
import mysql.connector
import warnings
from os import system
warnings.filterwarnings("ignore")

try:
    mydb = mysql.connector.connect(host=en.host, user=en.user, passwd=en.passwd, database=en.database)
    mycursor = mydb.cursor()
except:
    print("An error occured.")
    exit(0)

def db_connect(query_id):
    query = "select * from {} where id={}".format("diagnosis", query_id)
    global mycursor
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for x in myresult:
        sol = (mlp.predict([[x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]]]))
        sol = float(sol)

    query = "update diagnosis set PredictedOutcome = {} where id = {}".format(sol, query_id)
    mycursor.execute(query)
    mydb.commit()


if __name__ == "__main__":
    system("hostname -I")
    temp = (a[1])
    temp = temp.split(',')
    diabetes = pd.read_csv('~/hive-ml/diabetes.csv')
    X_train, X_test, y_train, y_test = train_test_split(diabetes.loc[:, diabetes.columns != 'Outcome'], diabetes['Outcome'], stratify=diabetes['Outcome'], random_state=66)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)

    global mlp
    mlp = MLPClassifier(random_state=66)
    mlp.fit(X_train_scaled, y_train)
    print("Accuracy on training set: {:.3f}".format(mlp.score(X_train_scaled, y_train)))
    print("Accuracy on test set: {:.3f}".format(mlp.score(X_test_scaled, y_test)))
    print("Computing ", len(a[1]), " results.")
    for queries in temp:
	    db_connect(queries)

    # terminate db connection
    mycursor.close()
    mydb.close()
    print("\n")
