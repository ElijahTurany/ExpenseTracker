import mysql.connector
from mysql.connector import Error
import pandas as pd

#Stolen
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
#query = "CREATE DATABASE ExpenseTracker"
#create_database(connection, query)

connection = create_db_connection("localhost", "root", "password", "ExpenseTracker")

# amount = input('Enter an amount: ')
# account = input('Enter an account: ')
# description = input('Enter an description: ')
# category = input('Enter an category: ')
# timestamp = input('Enter an timestamp (Optional): ')
# notes = input('Enter any notes (Optional): ')
