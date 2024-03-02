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


def clearTables():
    connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
    clearTables = """
        TRUNCATE TABLE Account;
        TRUNCATE TABLE Transaction;
        TRUNCATE TABLE Category;
        TRUNCATE TABLE User;
    """
    execute_query(connection, clearTables)

def deleteTables():
    connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
    clearTables = """
        DROP TABLE Account;
        DROP TABLE Transaction;
        DROP TABLE Category;
        DROP TABLE User;
    """
    execute_query(connection, clearTables)

# connection = create_server_connection("localhost", "root", "password")
# query = "CREATE DATABASE ExpenseTracker"
# execute_query(connection, query)

connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")

createAccountTable = """
CREATE TABLE Account (
    AccountId int(10) NOT NULL PRIMARY KEY ,
    title VARCHAR(20) NOT NULL,
    balance int(15) NOT NULL,
    UserId int(10) NOT NULL
);
"""

createTransactionTable = """
CREATE TABLE Transaction (
    transactionNum int(10) NOT NULL PRIMARY KEY ,
    amount int(10),
    description VARCHAR(250),
    accountId int(10),
    categoryId int(10),
    timestamp VARCHAR(30),
    note VARCHAR(100)
);
"""

createCategoryTable = """
CREATE TABLE Category (
    categoryId int(10) NOT NULL PRIMARY KEY ,
    name VARCHAR(25)
);
"""

createUserTable = """
CREATE TABLE User (
    userId int(10) NOT NULL PRIMARY KEY ,
    numberOfAccounts int(8),
    levelOfAccess int(2)
);
"""

#deleteTables()
#execute_query(connection, createAccountTable)
#execute_query(connection, createTransactionTable)
#execute_query(connection, createCategoryTable)
#execute_query(connection, createUserTable)

# amount = input('Enter an amount: ')
# account = input('Enter an account: ')
# description = input('Enter an description: ')
# category = input('Enter an category: ')
# timestamp = input('Enter an timestamp (Optional): ')
# notes = input('Enter any notes (Optional): ')
