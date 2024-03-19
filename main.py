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

#Creates the tables with the necessary information, NEED TO ADD TRANSFER TABLE!!!!!!!!!!#
#####################################################################################
def buildTables(connection):
    createAccountTable = """
    CREATE TABLE Account (
        AccountId int(10) NOT NULL,
        title VARCHAR(20) NOT NULL,
        balance int(15) NOT NULL,
        UserId int(10) NOT NULL,
        Primary Key (AccountId)
        Foreign Key (UserId) references User(userId)
    );
    """
    createTransactionTable = """
    CREATE TABLE Transaction (
        transactionNum int(10) NOT NULL,
        amount int(10),
        description VARCHAR(250),
        accountId int(10),
        categoryId int(10),
        timestamp VARCHAR(30),
        note VARCHAR(100),
        Primary Key (transactionNum)
        Foreign Key (accountId) references Account(AccountId)
        Foreign Key (categoryId) references Category(categoryId)
    );
    """
    createCategoryTable = """
    CREATE TABLE Category (
        categoryId int(10) NOT NULL,
        name VARCHAR(25),
        Primary Key (categoryId)
    );
    """
    createUserTable = """
    CREATE TABLE User (
        userId int(10) NOT NULL,
        numberOfAccounts int(8),
        levelOfAccess int(2) NOT NULL,
        Primary Key (userId)
    );
    """

    #execute_query(connection, createAccountTable)
    #execute_query(connection, createTransactionTable)
    #execute_query(connection, createCategoryTable)
    #execute_query(connection, createUserTable)

#Command out of sync error
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

#Typechecking in the GUI
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

def viewAccounts(connection):
    query = "SELECT * FROM account"
    return read_query(connection, query)

def viewTransactions(connection, timeframeStart, timeframeEnd, accountId, categoryId):
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
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
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
    query = "SELECT * FROM transaction WHERE 1=1"

    if (amountLow is not None) and (amountHigh is not None):
        query += " AND amount BETWEEN " + str(amountLow) + " AND " + str(amountHigh)
    elif (amountLow is not None):
        query += " AND amount >= " + str(amountLow)
    elif (amountHigh is not None):
        query += " AND amount <= " + str(amountHigh)

    if (description is not None):
        query += " AND description = '" + str(description) + "'"

    if (accountIds is not None):
        query += " AND ("
        for i in accountIds:
            query += "accountId = " + str(i) + " OR "
        query += "0=1)"

    if (categoryIds is not None):
        query += " AND ("
        for i in categoryIds:
            query += "categoryId = " + str(i) + " OR "
        query += "0=1)"

    if (timeframeStart is not None) and (timeframeEnd is not None):
        query += " AND timestamp BETWEEN " + str(timeframeStart) + " AND " + str(timeframeEnd)
    elif (timeframeStart is not None):
        query += " AND timestamp >= " + str(timeframeStart)
    elif (timeframeEnd is not None):
        query += " AND timestamp <= " + str(timeframeEnd)

    if (orderBy is not None):
        query += " ORDER BY " + str(orderBy)

    if (ascDesc is not None):
        query += " " + str(ascDesc)

    return read_query(connection, query)

def viewCategories(connection):
    query = "SELECT * FROM category"
    return read_query(connection, query)

def renameAccount(connection, AccountId_, newAccountName):
    query = "UPDATE Account SET accountName = newAccountName WHERE AccountId = AccountId_"
    return read_query(connection, query)
def editTransaction(connection, transactionNum_, newAmount, newDescription, accountId_, categoryId_, newTimestamp, newNote):
    query = "UPDATE Transaction SET amount = newAmount, description = newDescription, timestamp = newTimestamp, note = newNote WHERE transactionNum = transactionNum_"
    return read_query(connection, query)
def renameCategory(connection, categoryId_, newCategoryName):
    query = "UPDATE Category SET categoryName = newCategoryName WHERE categoryId = categoryId_"
    return read_query(connection, query)

# used mostly for testing purposes
# different methods later to clear data from the GUI but not from actual database
def deleteAccount(connection, AccountId_):
    query = "DELETE from Account WHERE AccountId = AccountId_"
    return read_query(connection, query)
def deleteTransaction(connection, transactionNum_):
    query = "DELETE from Transaction WHERE transactionNum = transactionNum_"
    return read_query(connection, query)
def deleteCategory(connection, categoryId_):
    query = "DELETE from Category WHERE categoryId = categoryId_"
    return read_query(connection, query)

def timeSummary():
    pass
def categorySummary():
    pass

# createDatabase("expensetracker")
connection = create_db_connection("localhost", "root", "MyDB2024", "expensetracker")
#buildTables(connection)
clearTables(connection)
addUser(connection, 0, 0, 1)
addAccount(connection, 0, "Wallet", 9, 0)
addCategory(connection, 0, "Snacks")
addTransaction(connection, 0, 2, "Candy bar", 0, 0, 100, "")
addTransaction(connection, 1, 119, "Groceries", 1, 1, 110, "Walmart")
addTransaction(connection, 2, 6, "Paper Towels", 1, 5, 110, "Walmart")
addTransaction(connection, 3, 2, "Sewing kit", 0, 4, 120, "")
addTransaction(connection, 4, 42, "Gas", 3, 2, 130, "Kwik Trip")
addTransaction(connection, 5, 24, "Acoustic Cafe", 0, 3, 140, "")

accounts = viewAccounts(connection)
for account in accounts:
    print(account)

categories = viewCategories(connection)
for category in categories:
    print(category)

transactions = viewTransactions(connection, 50, 150, 0, 0)
for transaction in transactions:
    print(transaction)

accountIds = [0, 1, 2]
categoryIds = [0, 1, 2, 3, 4]
transactions = advancedViewTransactions(connection, None, None, None, accountIds, categoryIds, None, None, "amount", "DESC")
for transaction in transactions:
    print(transaction)
