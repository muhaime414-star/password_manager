import sqlite3
import os

DB_NAME = "vault.db"

def init_db():
    """Creates the database and necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    


    
    cursor.execute('''CREATE TABLE IF NOT EXISTS master_salt 
                      (id INTEGER PRIMARY KEY, salt BLOB)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS vault 
                      (service TEXT PRIMARY KEY, username TEXT, encrypted_password BLOB)''')
    
    cursor.execute('SELECT salt FROM master_salt WHERE id=1')
    if not cursor.fetchone():
        salt = os.urandom(16)
        cursor.execute('INSERT INTO master_salt (id, salt) VALUES (?, ?)', (1, salt))
    
    conn.commit()
    conn.close()

def get_salt() -> bytes:
    """Retrieves the salt needed for PBKDF2."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT salt FROM master_salt WHERE id=1')
    salt = cursor.fetchone()[0]
    conn.close()
    return salt

def save_password(service, username, encrypted_password):
    """Saves or updates a credential in the vault."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO vault (service, username, encrypted_password) VALUES (?, ?, ?)', 
                   (service, username, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_password(service):
    """Fetches the ciphertext for a specific service."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, encrypted_password FROM vault WHERE service=?', (service,))
    result = cursor.fetchone()
    conn.close()
    return result
