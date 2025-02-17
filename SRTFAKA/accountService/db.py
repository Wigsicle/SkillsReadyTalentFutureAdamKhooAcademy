import sqlite3
import os
import pathlib

currentPath = os.path.dirname(os.path.abspath(__file__))

class AccountDB:
    def __init__(self):
        # SQLite database file (creates a new file if it doesn't exist)
        db_path = currentPath + '/accounts.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # To access rows as dictionaries
        self.cursor = self.conn.cursor()

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS accounts (
            accountId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            accountStatus BOOLEAN NOT NULL
        );
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'accounts' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def getAccountById(self, accountId):
        """Fetch account details by accountId."""
        try:
            sql = 'SELECT * FROM accounts WHERE accountId = ?'
            self.cursor.execute(sql, (accountId,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except sqlite3.Error as e:
            print(f"Database error during getAccountById: {e}")
            self.conn.rollback()
            return False

    def getAccountByUsername(self, username):
        """Fetch account details by username."""
        try:
            sql = 'SELECT * FROM accounts WHERE username = ?'
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except sqlite3.Error as e:
            print(f"Database error during getAccountByUsername: {e}")
            self.conn.rollback()
            return False

    def createAccount(self, accountData):
        """Insert a new account into the database."""
        sql = '''
            INSERT INTO accounts (accountId, name, username, password, accountStatus) 
            VALUES (?, ?, ?, ?, ?)
        '''
        try:
            self.cursor.execute(sql, accountData)
            self.conn.commit()
            return accountData[0]  # Return created account's accountId
        except sqlite3.Error as e:
            print(f"Database error during createAccount: {e}")
            self.conn.rollback()
            return False

    def updateAccount(self, accountId, updateData):
        """Update account information for the given accountId."""
        sql = '''
            UPDATE accounts 
            SET name = ?, password = ?
            WHERE accountId = ?
        '''
        try:
            self.cursor.execute(sql, (updateData['name'], updateData['password'], accountId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was updated
        except sqlite3.Error as e:
            print(f"Database error during updateAccount: {e}")
            self.conn.rollback()
            return False

    def deleteAccount(self, accountId):
        """Delete account by accountId."""
        sql = 'DELETE FROM accounts WHERE accountId = ?'
        try:
            self.cursor.execute(sql, (accountId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was deleted
        except sqlite3.Error as e:
            print(f"Database error during deleteAccount: {e}")
            self.conn.rollback()
            return False
    
    def close(self):
        self.cursor.close()
        self.conn.close()
