import mysql.connector
from mysql.connector import Error
import pandas as pd

startingBalanceCategoryId = 1
transferCategoryId = 2

functionalCategories = 2

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
def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#Create empty database
def createDatabase(name):
    connection = create_server_connection("localhost", "root", "MyDB2024")
    query = "CREATE DATABASE " + name
    executeQuery(connection, query)     

#Creating tables for the databse
def buildTables(connection):
    createAccountsTable = """
    CREATE TABLE accounts (
        accountId int NOT NULL AUTO_INCREMENT,
        title VARCHAR(20) NOT NULL,
        Primary Key (accountId)
    );
    """

    createCustomerTable = """
    CREATE TABLE customer (
        cusId int NOT NULL AUTO_INCREMENT,
        fname VARCHAR(20) NOT NULL,
        lname VARCHAR(20) NOT NULL,
        dob VARCHAR(20) NOT NULL,
        email VARCHAR(20) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        city VARCHAR(20) NOT NULL,
        state VARCHAR(20) NOT NULL,
        zipcode VARCHAR(20) NOT NULL,
        street VARCHAR(20) NOT NULL,
        Primary Key (cusId) 
    );
    """

    createCategoriesTable = """
    CREATE TABLE categories (
        categoryId int NOT NULL AUTO_INCREMENT,
        name VARCHAR(25) NOT NULL,
        Primary Key (categoryId)
    );
    """

    createTransactionsTable = """
    CREATE TABLE transactions (
        transactionNum int NOT NULL AUTO_INCREMENT,
        amount int NOT NULL,
        description VARCHAR(250) NOT NULL,
        accountId int NOT NULL,
        categoryId int NOT NULL,
        timestamp int NOT NULL,
        note VARCHAR(100),
        Primary Key (transactionNum),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (categoryId) references categories(categoryId)
    );
    """

    createTransferTable = """
    CREATE TABLE MoneyTransfer (
        transNum int NOT NULL AUTO_INCREMENT,
        cusId int NOT NULL,
        Acc1IdFrom int NOT NULL,
        Acc2IdTo int NOT NULL,
        amount int NOT NULL,
        timestamp int NOT NULL,
        Foreign Key (cusId) references customer(cusId),
        Foreign Key (Acc1IdFrom) references accounts(accountId),
        Foreign Key (Acc2IdTo) references accounts(accountId),
        Primary Key (transNum) 
    );
    """
    
    createUsersTable = """
    CREATE TABLE users (
        userId int NOT NULL AUTO_INCREMENT,
        fname VARCHAR(20) NOT NULL,
        lname VARCHAR(20) NOT NULL,
        email VARCHAR(20) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        city VARCHAR(20) NOT NULL,
        state VARCHAR(20) NOT NULL,
        zipcode VARCHAR(20) NOT NULL,
        street VARCHAR(20) NOT NULL,
        type int NOT NULL NOT NULL,
        title VARCHAR(30) NOT NULL,
        Primary Key (userId)
    );
    """

    createRegisteredAccountsTable = """
    CREATE TABLE registeredusers (
        cusId int NOT NULL AUTO_INCREMENT,
        accountId int NOT NULL,
        creationTimestamp int NOT NULL,
        Primary Key (accountId, cusId),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (cusId) references customer(cusId)
    );
    """

    #Creates category for starting balance transactions
    populateCategories = "INSERT INTO categories(name) VALUES('Starting Balance'), ('Transfer');"


    executeQuery(connection, createAccountsTable)
    executeQuery(connection, createCustomerTable)
    executeQuery(connection, createTransferTable)
    executeQuery(connection, createCategoriesTable)
    executeQuery(connection, createTransactionsTable)
    executeQuery(connection, createUsersTable)
    executeQuery(connection, createRegisteredAccountsTable)

    executeQuery(connection, populateCategories)


#Command out of sync error
def clearTables(connection):
    clearTables = """
        TRUNCATE TABLE accounts;
        TRUNCATE TABLE transactions;
        TRUNCATE TABLE categories;
        TRUNCATE TABLE users;
        TRUNCATE TABLE customer;
        TRUNCATE TABLE moneytransfer;
    """
    executeQuery(connection, clearTables)

def deleteTables(connection):
    clearTables = """
        DROP TABLE accounts;
        DROP TABLE transactions;
        DROP TABLE categories;
        DROP TABLE users;
        DROP TABLE customer;
        DROP TABLE moneytransfer;
    """
    executeQuery(connection, clearTables)

#Check for duplicate account names
def addAccount(connection, title, startingBalance):
    addQuery = "INSERT INTO accounts(title) VALUES('" + title + "')"
    executeQuery(connection, addQuery)
    if(startingBalance is not None):
        getIdQuery = "SELECT MAX(accountId) FROM accounts" 
        accountId = readQuery(connection, getIdQuery)
        addTransaction(connection, startingBalance, "Starting Balance", accountId[0][0], startingBalanceCategoryId, 0, None)

#Adding a transaction
def addTransaction(connection, amount, description, accountId, categoryId, timestamp, note):
    if(note is not None):
        query = "INSERT INTO transactions(amount, description, accountId, categoryId, timestamp, note) VALUES(" + str(amount) + ", '" + description + "', " + str(accountId) + ", " + str(categoryId) + ", " + str(timestamp) + ", '" + note +"')"
    else:
        query = "INSERT INTO transactions(amount, description, accountId, categoryId, timestamp) VALUES(" + str(amount) + ", '" + description + "', " + str(accountId) + ", " + str(categoryId) + ", " + str(timestamp) + ")"
    executeQuery(connection, query) 

#Check for duplicate category names
def addCategory(connection,name):
    query = "INSERT INTO categories(name) VALUES( '" + name + "')"
    executeQuery(connection, query)

#Adding a user
def addUser(connection, firstName, lastName, email, phone, city, state, zipcode, street, type, title):
    query = "INSERT INTO users(fname, lname, email, phone, city, zipcode, street, type, title) VALUES('" + firstName + "',  '" + lastName + "', '" + email + "', " + str(phone) + ", '" + city + "', '" + state + "', " + str(zipcode) + ", '" + street + "', " + str(type) + ", '" + title + "')"
    executeQuery(connection, query)

#I think the addTransactions should work, if not, just input like a cull value for categoryId
def addTransfer(connection, transNum, cusId, Acc1IdFrom, Acc2IdTo, amount, timestamp):
    query = "INSERT INTO MoneyTransfer(transNum, cusId, Acc1IdFrom, Acc2IdTo, amount, timestamp) VALUES('" + str(transNum) + "',  '" + str(cusId) + "', '" + str(Acc1IdFrom) + "', " + str(Acc2IdTo) + ", '" + str(amount) + "', '" + str(timestamp) + "')"
    removedAmt = amount * (-1)
    addTransaction(connection, removedAmt, "transfer", Acc1IdFrom, timestamp)
    addTransaction(connection, amount, "transfer", Acc2IdTo, timestamp)
    executeQuery(connection, query)

def addCustomer(connection, cusId, firstName, lastName, dob, email, phone, city, state, zipcode, street):
    query = "INSERT INTO customer(cusId, fname, lname, dob, email, phone, city, zipcode, street) VALUES('" + str(cusId) + "',  '" + firstName + "',  '" + lastName + "', '" + dob + "', '" + email + "', " + str(phone) + ", '" + city + "', '" + state + "', " + str(zipcode) + ", '" + street + "')"
    executeQuery(connection, query)


#View functions
def viewAccounts(connection):
    query = "SELECT * FROM accounts"
    return readQuery(connection, query)

def viewTransactions(connection, timeframeStart, timeframeEnd, accountId, categoryId):
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
    query = "SELECT * FROM transactions WHERE 1=1"

    if(timeframeStart is not None) and (timeframeEnd is not None):
        query += " AND timestamp BETWEEN " + str(timeframeStart) + " AND " + str(timeframeEnd)
    elif(timeframeStart is not None):
        query += " AND timestamp >= " + str(timeframeStart)
    elif(timeframeEnd is not None):
        query += " AND timestamp <= " + str(timeframeEnd)

    if(accountId is not None):
        query += " AND accountId=" + str(accountId) 
        
    if(categoryId is not None):
        query += " AND categoryId='" + str(categoryId) + "'"

    return readQuery(connection, query) 

def advancedViewTransactions(connection, amountLow, amountHigh, description, accountIds, categoryIds, timeframeStart, timeframeEnd, orderBy, ascDesc, note, showAllCategories):
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
    query = "SELECT t.transactionNum, t.amount, t.description, a.title, c.name, t.timestamp, t.note FROM transactions t"
    query += " JOIN accounts a  ON a.accountId = t.accountId JOIN categories c ON c.categoryId = t.categoryId"

    query += " WHERE 1=1"

    if(amountLow is not None) and (amountHigh is not None):
        query += " AND t.amount BETWEEN " + str(amountLow) + " AND " + str(amountHigh)
    elif(amountLow is not None):
        query += " AND t.amount >= " + str(amountLow)
    elif(amountHigh is not None):
        query += " AND t.amount <= " + str(amountHigh)

    if(description is not None):
        query += " AND t.description LIKE '" + str(description) + "'"

    if(accountIds is not None):
        query += " AND ("
        for i in accountIds:
            query += "t.accountId = " + str(i) + " OR "
        query += "0=1)"

    if(categoryIds is not None):
        query += " AND ("
        for i in categoryIds:
            query += "t.categoryId = " + str(i) + " OR "
        query += "0=1)"

    if(timeframeStart is not None) and (timeframeEnd is not None):
        query += " AND t.timestamp BETWEEN " + str(timeframeStart) + " AND " + str(timeframeEnd)
    elif(timeframeStart is not None):
        query += " AND t.timestamp >= " + str(timeframeStart)
    elif(timeframeEnd is not None):
        query += " AND t.timestamp <= " + str(timeframeEnd)

    if(note is not None):
        query += " AND t.note LIKE '" + str(note) + "'"

    if(showAllCategories is False):
        query += " AND t.categoryId > " + str(functionalCategories)

    if(orderBy is not None):
        query += " ORDER BY " + str(orderBy)

    if(ascDesc is not None):
        query += " " + str(ascDesc)

    return readQuery(connection, query)

def viewCategories(connection):
    query = "SELECT * FROM categories"
    return readQuery(connection, query)

def viewTransfers(connection):
    query = "SELECT * FROM moneyTransfers"
    return readQuery(connection, query)

def viewCustomers(connection):
    query = "SELECT * FROM customer"
    return readQuery(connection, query)

def viewBalance(connection, accountId):
    query = """
        SELECT SUM(amount) as balance
        FROM expensetracker.transactions
        WHERE accountId = """ + str(accountId)
    return readQuery(connection, query)[0][0]

def viewBalances(connection):
    query = """
        SELECT a.accountId, a.title, sum(t.amount) as balance
        FROM expensetracker.transactions t
        JOIN accounts a ON a.accountId = t.accountId
        GROUP BY t.accountId;
    """
    return readQuery(connection, query)

#Only update if value isn't none
#Change to update with passed in values
def renameAccount(connection, AccountId_, newAccountName):
    query = "UPDATE accounts SET accountName = newAccountName WHERE AccountId = AccountId_"
    return readQuery(connection, query)

#Only update if value isn't none
#Change to update with passed in values
def editTransaction(connection, transactionNum_, newAmount, newDescription, accountId_, categoryId_, newTimestamp, newNote):
    query = "UPDATE transactions SET amount = newAmount, description = newDescription, timestamp = newTimestamp, note = newNote WHERE transactionNum = transactionNum_"
    return readQuery(connection, query)

#Only update if value isn't none
#Change to update with passed in values
def renameCategory(connection, categoryId_, newCategoryName):
    query = "UPDATE categories SET categoryName = newCategoryName WHERE categoryId = categoryId_"
    return readQuery(connection, query)

def editTransfer(connection, transNum_, cusId_, Acc1IdFrom_, Acc2IdTo_, amount_, timestamp_):
    query = "UPDATE MoneyTransfer SET amount = amount_, timestamp = timestamp_ where transNum = transNum_"
    return readQuery(connection, query)

def editCustomer():
    pass

def editUser():
    pass

# used mostly for testing purposes
# different methods later to clear data from the GUI but not from actual database

#Update to delete a given account
def deleteAccount(connection, AccountId_):
    query = "DELETE from accounts WHERE AccountId = AccountId_"
    return readQuery(connection, query)

#Update to delete a given transaction
def deleteTransaction(connection, transactionNum_):
    query = "DELETE from transactions WHERE transactionNum = transactionNum_"
    return readQuery(connection, query)

#Update to delete a given category
def deleteCategory(connection, categoryId_):
    query = "DELETE from categories WHERE categoryId = categoryId_"
    return readQuery(connection, query)

#Update to delete a given transfer
def deleteTransfer(connection, transNum_):
    query = "DELETE from MoneyTransfer WHERE transNum = transNum_"
    return readQuery(connection, query)

def timeSummary():
    pass

def categorySummary():
    pass

def populateTables(connection):
    addUser(connection, "first", "last", "abc@email.com", 15551239876, "city", "state", 12345, "street", 0, "title")
    addAccount(connection, "Wallet", 50)
    addAccount(connection, "DebitCard", 200)
    addAccount(connection, "CreditCard", None)
    addCategory(connection, "Snacks")
    addCategory(connection, "Food")
    addCategory(connection, "Gas")
    addCategory(connection, "Restaurant")
    addCategory(connection, "Cats")
    addCategory(connection, "Home")
    addTransaction(connection, -2, "Candy bar", 1, 3, 100, None)
    addTransaction(connection, -119, "Groceries", 2, 4, 110, "Walmart")
    addTransaction(connection, -6, "Paper Towels", 2, 8, 110, "Walmart")
    addTransaction(connection, -26, "Cat Litter", 2, 7, 120, None)
    addTransaction(connection, -42, "Gas", 3, 5, 130, "Kwik Trip")
    addTransaction(connection, -24, "Acoustic Cafe", 1, 6, 140, None)

def printTables(connection):
    accounts = viewAccounts(connection)
    for account in accounts:
        print(account)

    categories = viewCategories(connection)
    for category in categories:
        print(category)

    transactions = viewTransactions(connection, None, None, None, None)
    for transaction in transactions:
        print(transaction)

    accountIds = [0, 1]
    categoryIds = [0, 1, 2, 3, 4]
    transactions = advancedViewTransactions(connection, None, None, None, accountIds, categoryIds, None, None, "amount", "DESC", None)
    for transaction in transactions:
        print(transaction)