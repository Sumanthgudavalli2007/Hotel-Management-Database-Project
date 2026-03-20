import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=LAPTOP-9AFL8P78;"   # 🔁 Change if needed
        "Database=HotelManagementDB;"
        "Trusted_Connection=yes;"
    )

def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    conn.commit()
    conn.close()