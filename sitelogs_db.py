import urllib2
import sqlite3
connection = sqlite3.connect('sitelogs.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE Sitelogs
    (url VARCHAR(255),
    status_code INTEGER,
    timestamp VARCHAR(29)
    )''')

print "before commit"
connection.commit()
print "after commit"

# # Create table
# cursor.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')

# # Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# conn.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# conn.close()

