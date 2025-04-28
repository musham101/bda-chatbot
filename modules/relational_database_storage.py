import mysql.connector
from mysql.connector import errorcode

class RelationalDatabaseStorage:
    def create_database(config):
        try:
            conn = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
            print(f"✅ Database '{config['database']}' created or already exists.")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"❌ Failed to create database: {err}")

    def connect_to_db(config):
        try:
            conn = mysql.connector.connect(**config)
            print("✅ Connected to database.")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Connection failed: {err}")
            return None
        
    def create_tables(conn):
        try:
            cursor = conn.cursor()

            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL UNIQUE,
                name VARCHAR(100),
                email VARCHAR(100),
                signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Sessions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id VARCHAR(100) PRIMARY KEY,
                user_id VARCHAR(100),
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """)

            conn.commit()
            cursor.close()
            print("✅ Tables created.")
        except mysql.connector.Error as err:
            print(f"❌ Failed to create tables: {err}")
    
    def setup_chatbot_db(config):
        RelationalDatabaseStorage.create_database(config)
        conn = RelationalDatabaseStorage.connect_to_db(config)
        if conn:
            RelationalDatabaseStorage.create_tables(conn)
            conn.close()