import pyodbc

"""
Non funcitonal examples of how SQL Server could be used to store the scraped data.
"""

def connect():
    """
    Connect to SQL Server
    """
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=master;UID=sa;PWD=Password123')
    return cnxn

def store(data):
    """
    Store data in SQL Server
    """
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO dbo.data (data) VALUES ('{}')".format(data))
    cnxn.commit()
    cnxn.close()

def store_many(data):
    """
    Store data in SQL Server
    """
    cnxn = connect()
    cursor = cnxn.cursor()
    cursor.executemany("INSERT INTO dbo.data (data) VALUES ('{}')".format(data))
    cnxn.commit()
    cnxn.close()
