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


def createDatabase(name):
    connection = create_server_connection("localhost", "root", "MyDB2024")
    query = "CREATE DATABASE " + name
    execute_query(connection, query)     

#Creating tables for the databse
def buildTables(connection):
    createAccountsTable = """
    CREATE TABLE accounts (
        accountId int(10) NOT NULL AUTO_INCREMENT,
        title VARCHAR(20) NOT NULL,
        Primary Key (accountId),
    );
    """
    createTransferTable = """
    CREATE TABLE MoneyTransfer (
        transNum int(10) NOT NULL AUTO_INCREMENT,
        cusId int(10) NOT NULL,
        Acc1IdFrom int(10) NOT NULL,
        Acc2IdTo int(10) NOT NULL,
        amount int(5),
        dateOfTransfer DATE NOT NULL,
        Foreign Key (cusId) references customer(cusId),
        Foreign Key (Acc1IdFrom) references accounts(accountId),
        Foreign Key (Acc2IdTo) references accounts(accountId),
        Primary Key (transNum) 
    );
    """

    createCustomerTable = """
    CREATE TABLE customer (
        cusId int(10) NOT NULL AUTO_INCREMENT,
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
    createTransactionsTable = """
    CREATE TABLE transactions (
        transactionNum int(10) NOT NULL AUTO_INCREMENT,
        amount int(10),
        description VARCHAR(250),
        accountId int(10),
        categoryId int(10),
        dateOfTransaction DATETIME,
        note VARCHAR(100),
        Primary Key (transactionNum),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (categoryId) references categories(categoryId)
    );
    """
    createCategoriesTable = """
    CREATE TABLE categories (
        categoryId int(10) NOT NULL AUTO_INCREMENT,
        name VARCHAR(25),
        Primary Key (categoryId)
    );
    """
    createUsersTable = """
    CREATE TABLE users (
        userId int(10) NOT NULL AUTO_INCREMENT,
        fname VARCHAR(20) NOT NULL,
        lname VARCHAR(20) NOT NULL,
        email VARCHAR(20) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        city VARCHAR(20) NOT NULL,
        state VARCHAR(20) NOT NULL,
        zipcode VARCHAR(20) NOT NULL,
        street VARCHAR(20) NOT NULL,
        type int(2) NOT NULL,
        title VARCHAR(30) NOT NULL,
        Primary Key (userId)
    );
    """

    createRegisteredAccountsTable = """
    CREATE TABLE users (
        cusId int(10) NOT NULL AUTO_INCREMENT,
        accountId int(10) NOT NULL,
        dateCreation DATE,
        Primary Key (accountId, cusId),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (cusId) references customer(cusId)

    );
    """

    execute_query(connection, createAccountsTable)
    execute_query(connection, createTransferTable)
    execute_query(connection, createCustomerTable)
    execute_query(connection, createTransactionsTable)
    execute_query(connection, createCategoriesTable)
    execute_query(connection, createUsersTable)
    

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
    execute_query(connection, clearTables)
def deleteTables(connection):
    clearTables = """
        DROP TABLE accounts;
        DROP TABLE transactions;
        DROP TABLE categories;
        DROP TABLE users;
        DROP TABLE customer;
        DROP TABLE moneytransfer;
    """
    execute_query(connection, clearTables)

#Typechecking in the GUI
#Add starting balance transaction
def addAccount(connection, accountId, title, userId):
    query = "INSERT INTO accounts VALUES(" + str(accountId) + ",  '" + title + "', " + str(userId) + ")"
    execute_query(connection, query) 
def addTransaction(connection, transactionId, amount, description, accountId, categoryId, timestamp, note):
    query = "INSERT INTO transactions VALUES(" + str(transactionId) + ",  " + str(amount) + ", '" + description + "', " + str(accountId) + ", " + str(categoryId) + ", " + str(timestamp) + ", '" + note +"')"
    execute_query(connection, query) 
    print(query)
def addCategory(connection, categoryId, name):
    query = "INSERT INTO categories VALUES(" + str(categoryId) + ",  '" + name + "')"
    execute_query(connection, query)
def addUser(connection, userId, firstName, lastName, email, phone, city, state, zipcode, street, type, title):
    query = "INSERT INTO users VALUES(" + str(userId) + ",  '" + firstName + "',  '" + lastName + "', '" + email + "', " + str(phone) + ", '" + city + "', '" + state + "', " + str(zipcode) + ", '" + street + "', " + str(type) + ", '" + title + "')"
    execute_query(connection, query)

def addTransfer():
    pass
def addCustomer():
    pass

def viewAccounts(connection):
    query = "SELECT * FROM accounts"
    return read_query(connection, query)
def viewTransactions(connection, timeframeStart, timeframeEnd, accountId, categoryId):
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
    query = "SELECT * FROM transactions WHERE 1=1"

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
def advancedViewTransactions(connection, amountLow, amountHigh, description, accountIds, categoryIds, timeframeStart, timeframeEnd, orderBy, ascDesc, note):
    #"WHERE 1=1" is added so adding filters is as simple as adding " AND condition"
    query = "SELECT t.transactionNum, t.amount, t.description, a.title, c.name, t.timestamp, t.note FROM transactions t"
    query += " JOIN accounts a  ON a.accountId = t.accountId JOIN categories c ON c.categoryId = t.categoryId"

    query += " WHERE 1=1"

    if (amountLow is not None) and (amountHigh is not None):
        query += " AND amount BETWEEN " + str(amountLow) + " AND " + str(amountHigh)
    elif (amountLow is not None):
        query += " AND amount >= " + str(amountLow)
    elif (amountHigh is not None):
        query += " AND amount <= " + str(amountHigh)

    if (description is not None):
        query += " AND description LIKE '" + str(description) + "'"

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

    if (note is not None):
        query += " AND note LIKE '" + str(note) + "'"

    if (orderBy is not None):
        query += " ORDER BY " + str(orderBy)

    if (ascDesc is not None):
        query += " " + str(ascDesc)

    return read_query(connection, query)
def viewCategories(connection):
    query = "SELECT * FROM categories"
    return read_query(connection, query)

def viewTransfers():
    pass
def viewCustomers():
    pass

def renameAccount(connection, AccountId_, newAccountName):
    query = "UPDATE accounts SET accountName = newAccountName WHERE AccountId = AccountId_"
    return read_query(connection, query)
def editTransaction(connection, transactionNum_, newAmount, newDescription, accountId_, categoryId_, newTimestamp, newNote):
    query = "UPDATE transactions SET amount = newAmount, description = newDescription, timestamp = newTimestamp, note = newNote WHERE transactionNum = transactionNum_"
    return read_query(connection, query)
def renameCategory(connection, categoryId_, newCategoryName):
    query = "UPDATE categories SET categoryName = newCategoryName WHERE categoryId = categoryId_"
    return read_query(connection, query)

def editTransfer():
    pass

# used mostly for testing purposes
# different methods later to clear data from the GUI but not from actual database
def deleteAccount(connection, AccountId_):
    query = "DELETE from accounts WHERE AccountId = AccountId_"
    return read_query(connection, query)
def deleteTransaction(connection, transactionNum_):
    query = "DELETE from transactions WHERE transactionNum = transactionNum_"
    return read_query(connection, query)
def deleteCategory(connection, categoryId_):
    query = "DELETE from categories WHERE categoryId = categoryId_"
    return read_query(connection, query)

def deleteTransfer():
    pass

def timeSummary():
    pass
def categorySummary():
    pass

def populateTables(connection):
    addUser(connection, 0, "first", "last", "abc@email.com", 15551239876, "city", "state", 12345, "street", 0, "title")
    addAccount(connection, 0, "Wallet", 0)
    addAccount(connection, 1, "DebitCard", 0)
    addAccount(connection, 2, "CreditCard", 0)
    addCategory(connection, 0, "Snacks")
    addCategory(connection, 1, "Food")
    addCategory(connection, 2, "Gas")
    addCategory(connection, 3, "Restaurant")
    addCategory(connection, 4, "Cats")
    addCategory(connection, 5, "Home")
    addTransaction(connection, 0, 2, "Candy bar", 0, 0, 100, "")
    addTransaction(connection, 1, 119, "Groceries", 1, 1, 110, "Walmart")
    addTransaction(connection, 2, 6, "Paper Towels", 1, 5, 110, "Walmart")
    addTransaction(connection, 3, 26, "Cat Litter", 0, 4, 120, "")
    addTransaction(connection, 4, 42, "Gas", 2, 2, 130, "Kwik Trip")
    addTransaction(connection, 5, 24, "Acoustic Cafe", 0, 3, 140, "")

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