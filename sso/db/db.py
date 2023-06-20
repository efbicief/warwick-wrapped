# pylint: disable=missing-function-docstring
import sqlite3

class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        if self.check_if_no_tables():
            self.initialise_new()

    def check_if_no_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchone() is None

    def initialise_new(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS uuid_token (uuid TEXT PRIMARY KEY, token TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS token_secret (token TEXT PRIMARY KEY, secret TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS share_tokens (share_code TEXT PRIMARY KEY, token TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_ids (uuid_token TEXT PRIMARY KEY, userId TEXT)")
        self.conn.commit()

    def get_token_for_uuid(self, uuid: str):
        self.cursor.execute("SELECT token FROM uuid_token WHERE uuid=?", (uuid,))
        resp = self.cursor.fetchone()
        if resp is None:
            return None
        return resp[0]

    def get_secret_for_token(self, token: str):
        self.cursor.execute("SELECT secret FROM token_secret WHERE token=?", (token,))
        resp = self.cursor.fetchone()
        if resp is None:
            return None
        return resp[0]

    def add_token_for_uuid(self, uuid: str, token: str):
        self.cursor.execute("INSERT INTO uuid_token VALUES (?, ?)", (uuid, token))
        self.conn.commit()

    def add_secret_for_token(self, token: str, secret: str):
        self.cursor.execute("INSERT INTO token_secret VALUES (?, ?)", (token, secret))
        self.conn.commit()

    def add_token_share_code(self, share_code: str, token: str):
        self.cursor.execute("INSERT INTO share_tokens VALUES (?, ?)", (share_code, token))
        self.conn.commit()
    
    def get_token_for_share_code(self, share_code: str):
        self.cursor.execute("SELECT token FROM share_tokens WHERE share_code=?", (share_code,))
        resp = self.cursor.fetchone()
        if resp is None:
            return None
        return resp[0]

    def add_user_id(self, uuid_token: str, userId: str):
        self.cursor.execute("SELECT * from user_ids WHERE userId=?", (userId,))
        resp = self.cursor.fetchone()
        if resp is not None:
            return
        self.cursor.execute("INSERT OR IGNORE INTO user_ids VALUES (?, ?)", (uuid_token, userId))
        self.conn.commit()

    def count_number_of_tokens(self):
        self.cursor.execute("SELECT COUNT(DISTINCT userId) FROM user_ids;")
        return self.cursor.fetchone()[0]