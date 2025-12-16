import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=COMP2001_CW2;"
        "UID=sa;"
        "PWD=YourStrong!Passw0rd"
    )
    return conn
