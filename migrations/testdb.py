import mysql.connector

# Configuration
config = {
    'host': 'zimba-rei-micro.host endpoint',
    'port': 3306,
    'user': 'rei_app_rds_user',
    'password': 'the password',
    'migrations': 'zimba_rei_micro'
}

try:
    # Establish a connection
    conn = mysql.connector.connect(**config)
    
    if conn.is_connected():
        print("Connected to MySQL migrations")
        
        # Perform some operation (e.g., select data)
        cursor = conn.cursor()
        query = "SELECT * FROM subscription LIMIT 5"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        
        cursor.close()
        conn.close()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL migrations: {err}")
