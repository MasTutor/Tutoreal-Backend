import mysql.connector
from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()
dbase = os.getenv("dbase")
duser = os.getenv("duser")
dpw = os.getenv("dpw")
dip = os.getenv("dip")

# Define a function to open database connection
def open_db_connection(db_name, user, password, host):
    # Try to connect to the database
    try:
        # Create a connection object with the name mydb
        mydb = mysql.connector.connect(database=db_name, user=user, password=password, host=host)
        # Print a success message
        print("Opened connection to database:", db_name)
        # Return the connection object
        return mydb
    # Handle any exceptions
    except mysql.connector.Error as e:
        # Print an error message
        print("Failed to open connection to database:", e)
        # Return None
        return None

# Define a function to close database connection
def close_db_connection(mydb, db_name):
    # Check if the connection object exists
    if mydb:
        # Try to close the connection
        try:
            # Close the connection
            mydb.close()
            # Print a success message
            print("Closed connection to database:", db_name)
        # Handle any exceptions
        except mysql.connector.Error as e:
            # Print an error message
            print("Failed to close connection to database:", e)



def defineDB():
   mydb=open_db_connection(
       dbase,
       duser,
       dpw,
       dip,
   )
   return mydb