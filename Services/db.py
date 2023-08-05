import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="arham@123",
        database="scangreeks"
    )


#
# cursor = mydb.cursor()
# query = '''INSERT INTO example values (%s, %s, %s, %s, %s)'''
# value = ("Ram", "CSE", "85", "B", "19")
# cursor.execute(query,value)
# mydb.commit()
# cursor.close()
# mydb.close()