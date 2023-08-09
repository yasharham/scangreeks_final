import urllib.parse
from sqlalchemy import create_engine
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="arham@123",
        database="scangreeks"
    )



host = "localhost"
username = "root"
password = "arham@123"
encoded_username = urllib.parse.quote(username)
encoded_password = urllib.parse.quote(password)
database = "scangreeks"


engine = create_engine(f'mysql+mysqlconnector://{encoded_username}:{encoded_password}@{host}/{database}')


#
# cursor = mydb.cursor()
# query = '''INSERT INTO example values (%s, %s, %s, %s, %s)'''
# value = ("Ram", "CSE", "85", "B", "19")
# cursor.execute(query,value)
# mydb.commit()
# cursor.close()
# mydb.close()