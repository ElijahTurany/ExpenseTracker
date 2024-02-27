import mysql.connector
from mysql.connector import Error
import pandas as pd

#Stolen
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#Also Stolen
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


#NOT stolen
def addTransaction():
    pass
def addAccount():
    pass
def addUser():
    pass
def addCategory():
    pass

# connection = create_server_connection("localhost", "root", "password")
# query = "CREATE DATABASE ExpenseTracker"
# execute_query(connection, query)

connection = create_db_connection("localhost", "root", "password", "expensetracker")

createAccountTable = """
CREATE TABLE Account (
    col0 VARCHAR(20),
    col1 VARCHAR(20),
    col2 VARCHAR(20),
    col3 VARCHAR(20)
);
"""

createTransactionTable = """
CREATE TABLE Transaction (
    col0 VARCHAR(20),
    col1 VARCHAR(20),
    col2 VARCHAR(20),
    col3 VARCHAR(20),
    col4 VARCHAR(20),
    col5 VARCHAR(20),
    col6 VARCHAR(20)
);
"""

createCategoryTable = """
CREATE TABLE Category (
    col0 VARCHAR(20),
    col1 VARCHAR(20)
);
"""

createUserTable = """
CREATE TABLE User (
    col0 VARCHAR(20),
    col1 VARCHAR(20),
    col2 VARCHAR(20)
);
"""

execute_query(connection, createAccountTable)
execute_query(connection, createTransactionTable)
execute_query(connection, createCategoryTable)
execute_query(connection, createUserTable)

# amount = input('Enter an amount: ')
# account = input('Enter an account: ')
# description = input('Enter an description: ')
# category = input('Enter an category: ')
# timestamp = input('Enter an timestamp (Optional): ')
# notes = input('Enter any notes (Optional): ')
