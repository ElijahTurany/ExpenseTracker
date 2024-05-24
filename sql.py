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

#Create empty database
def createDatabase(name):
    connection = create_server_connection("localhost", "root", "MyDB2024")
    query = "CREATE DATABASE " + name
    execute_query(connection, query)     

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
    createTransferTable = """
    CREATE TABLE MoneyTransfer (
        transNum int NOT NULL AUTO_INCREMENT,
        cusId int NOT NULL,
        Acc1IdFrom int NOT NULL,
        Acc2IdTo int NOT NULL,
        amount int,
        dateOfTransfer DATE NOT NULL,
        Foreign Key (cusId) references customer(cusId),
        Foreign Key (Acc1IdFrom) references accounts(accountId),
        Foreign Key (Acc2IdTo) references accounts(accountId),
        Primary Key (transNum) 
    );
    """

    createCategoriesTable = """
    CREATE TABLE categories (
        categoryId int NOT NULL AUTO_INCREMENT,
        name VARCHAR(25),
        Primary Key (categoryId)
    );
    """

    createTransactionsTable = """
    CREATE TABLE transactions (
        transactionNum int NOT NULL AUTO_INCREMENT,
        amount int,
        description VARCHAR(250),
        accountId int,
        categoryId int,
        dateOfTransaction DATETIME,
        note VARCHAR(100),
        Primary Key (transactionNum),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (categoryId) references categories(categoryId)
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
        type int NOT NULL,
        title VARCHAR(30) NOT NULL,
        Primary Key (userId)
    );
    """

    createRegisteredAccountsTable = """
    CREATE TABLE registeredusers (
        cusId int NOT NULL AUTO_INCREMENT,
        accountId int NOT NULL,
        dateCreation DATE,
        Primary Key (accountId, cusId),
        Foreign Key (accountId) references accounts(accountId),
        Foreign Key (cusId) references customer(cusId)
    );
    """


    execute_query(connection, createAccountsTable)
    execute_query(connection, createCustomerTable)
    execute_query(connection, createTransferTable)
    execute_query(connection, createCategoriesTable)
    execute_query(connection, createTransactionsTable)
    execute_query(connection, createUsersTable)
    execute_query(connection, createRegisteredAccountsTable)


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
def addAccount(connection, title, userId):
    query = "INSERT INTO accounts VALUES('" + title + "', " + str(userId) + ")"
    execute_query(connection, query) 
def addTransaction(connection, amount, description, accountId, categoryId, timestamp, note):
    query = "INSERT INTO transactions VALUES(" + str(amount) + ", '" + description + "', " + str(accountId) + ", " + str(categoryId) + ", " + str(timestamp) + ", '" + note +"')"
    execute_query(connection, query) 
    print(query)
def addCategory(connection,name):
    query = "INSERT INTO categories VALUES( '" + name + "')"
    execute_query(connection, query)
def addUser(connection, firstName, lastName, email, phone, city, state, zipcode, street, type, title):
    query = "INSERT INTO users VALUES('" + firstName + "',  '" + lastName + "', '" + email + "', " + str(phone) + ", '" + city + "', '" + state + "', " + str(zipcode) + ", '" + street + "', " + str(type) + ", '" + title + "')"
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
    addUser(connection, "first", "last", "abc@email.com", 15551239876, "city", "state", 12345, "street", 0, "title")
    addAccount(connection, "Wallet", 0)
    addAccount(connection, "DebitCard", 0)
    addAccount(connection, "CreditCard", 0)
    addCategory(connection, "Snacks")
    addCategory(connection, "Food")
    addCategory(connection, "Gas")
    addCategory(connection, "Restaurant")
    addCategory(connection, "Cats")
    addCategory(connection, "Home")
    addTransaction(connection, 2, "Candy bar", 0, 0, 100, "")
    addTransaction(connection, 119, "Groceries", 1, 1, 110, "Walmart")
    addTransaction(connection, 6, "Paper Towels", 1, 5, 110, "Walmart")
    addTransaction(connection, 26, "Cat Litter", 0, 4, 120, "")
    addTransaction(connection, 42, "Gas", 2, 2, 130, "Kwik Trip")
    addTransaction(connection, 24, "Acoustic Cafe", 0, 3, 140, "")

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