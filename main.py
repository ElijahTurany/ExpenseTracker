import mysql.connector
from mysql.connector import Error
import pandas as pd

#Stolen
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(user='root', password='MyDB2024',
                              host='localhost', database='HPDataBase')
       

        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_server_connection("localhost", "root", "MyDB2024")

#amount = input('Enter an amount: ')
#account = input('Enter an account: ')
#description = input('Enter an description: ')
#category = input('Enter an category: ')
#timestamp = input('Enter an timestamp (Optional): ')
#notes = input('Enter any notes (Optional): ')

