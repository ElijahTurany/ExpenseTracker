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

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#NOT stolen
def createDatabase(name):
    connection = create_server_connection("localhost", "root", "MyDB2024")
    query = "CREATE DATABASE " + name
    execute_query(connection, query)     

def buildTables(connection):
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

    execute_query(connection, createAccountTable)
    execute_query(connection, createTransactionTable)
    execute_query(connection, createCategoryTable)
    execute_query(connection, createUserTable)

def clearTables(connection):
    clearTables = """
        TRUNCATE TABLE Account;
        TRUNCATE TABLE Transaction;
        TRUNCATE TABLE Category;
        TRUNCATE TABLE User;
    """
    execute_query(connection, clearTables)

def deleteTables(connection):
    clearTables = """
        DROP TABLE Account;
        DROP TABLE Transaction;
        DROP TABLE Category;
        DROP TABLE User;
    """
    execute_query(connection, clearTables)

def addAccount(connection, accountId, title, balance, userId):
    query = "INSERT INTO account VALUES(" + str(accountId) + ",  '" + title + "', " + str(balance) + ", " + str(userId) + ")"
    execute_query(connection, query)
    
def addTransaction(connection, transactionId, amount, description, accountId, categoryId, timestamp, note):
    query = "INSERT INTO transaction VALUES(" + str(transactionId) + ",  " + str(amount) + ", '" + description + "', " + str(accountId) + ", " + str(categoryId) + ", " + str(timestamp) + ", '" + note +"')"
    execute_query(connection, query)
    
def addCategory(connection, categoryId, name):
    query = "INSERT INTO category VALUES(" + str(categoryId) + ",  '" + name + "')"
    execute_query(connection, query)

def addUser(connection, userId, numAccounts, levelOfAccess):
    query = "INSERT INTO user VALUES(" + str(userId) + ",  " + str(numAccounts) + ",  " + str(levelOfAccess) +")"
    execute_query(connection, query)

def renameAccount(connection, accountId, accountName):
    pass
def editTransaction(connection, transactionId, amount, description, accountId, categoryId, timestamp, note):
    pass
def renameCategory(connection, categoryId, categoryName):
    pass

def viewAccounts(connection):
    query = "SELECT * FROM account"
    return read_query(connection, query)

def viewTransactions(connection, timeframeStart, timeframeEnd, accountId, categoryId):
    if (accountId is None) and (timeframeStart is None) and (timeframeEnd is None) and (categoryId is None):
        query = "SELECT * FROM transaction"
        return read_query(connection, query) 
    else:
        query = "SELECT * FROM transaction WHERE 1=1"

        if (timeframeStart is not None) and (timeframeEnd is not None):
            query += " AND timestamp BETWEEN " + str(timeframeStart) + " AND " + str(timeframeEnd)
        elif (timeframeStart is not None):
            query += " AND timestamp >= " + str(timeframeStart)
        elif (timeframeEnd is not None):
            query += " AND timestamp <= " + str(timeframeEnd)

        if (accountId is not None):
            query += " AND accountId=" + str(accountId) 
        
        if (categoryId is not None):
            query += " AND categoryId='" + str(categoryId) + "'"

        return read_query(connection, query) 

def advancedViewTransactions(connection, amountLow, amountHigh, description, accountIds, categoryIds, timeframeStart, timeframeEnd, orderBy, ascDesc):
    query = "SELECT * FROM transaction WHERE 1=1"

    if (amountLow is not None) and (amountHigh is not None):
        query += " AND amount BETWEEN " + str(timeframeStart) + " AND " + str(timeframeEnd)
    elif (amountLow is not None):
        query += " AND amount >= " + str(timeframeStart)
    elif (amountHigh is not None):
        query += " AND amount <= " + str(timeframeEnd)

    if (description is not None):
        query += " AND description = " + str(description)



def viewCategories(connection):
    query = "SELECT * FROM category"
    return read_query(connection, query)

def deleteAccount(connection, accountId):
    pass
def deleteTransaction(connection, transactionId):
    pass
def deleteCategory(connection, categoryId):
    pass

def timeSummary():
    pass
def categorySummary():
    pass

# amount = input('Enter an amount: ')
# account = input('Enter an account: ')
# description = input('Enter an description: ')
# category = input('Enter an category: ')
# timestamp = input('Enter an timestamp (Optional): ')
# notes = input('Enter any notes (Optional): ')

createDatabase("expensetracker")
connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
buildTables(connection)
addUser(connection, 0, 0, 1)
addAccount(connection, 0, "Wallet", 9, 0)
addCategory(connection, 0, "Snacks")
addTransaction(connection, 0, 2, "Candy bar", 0, 0, 100, "")

accounts = viewAccounts(connection)
for account in accounts:
    print(account)

categories = viewCategories(connection)
for category in categories:
    print(category)

transactions = viewTransactions(connection, 50, 150, 0, 0)
for transaction in transactions:
    print(transaction)