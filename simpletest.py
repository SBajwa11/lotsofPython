import mysql.connector
from mysql.connector import Error

sortorder = input('Define sort order: ascending or descending ')
ascending = 'ascending'
descending = 'descending'
number_list = []
n = int(input("Enter amount of numbers to be entered "))
print("\n")

for i in range(0, n):
    print("Enter number", i+1, )
    item = int(input())
    number_list.append(item)
print("The list of numbers is ", number_list)
if sortorder == ascending:
    number_list.sort()
    print(number_list)
else:
    number_list.sort(reverse=True)
    print(number_list)

#User input for number list works effectively, with ascending and descending working without problem. Issue came with the mySQL Connection, see attached doc. 
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user = 'sabraaj.bajwa@gmail.com',
        password = 'reuben6868',
        database = 'sorteddata' )
    
    mysql_insert_query = """INSERT INTO sorteddata (value) VALUES (%s, %s, %s, %s, %s, %s) """
    cursor = connection.cursor()
    cursor.executemany(mysql_insert_query, number_list)
    connection.commit()
    print(cursor.rowcount, "Record added successfully")

except mysql.connector.Error as error: 
    print("Error in inserting record".format(error))

finally: 
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
