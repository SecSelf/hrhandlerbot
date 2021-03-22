import sqlite3

__connection = None


def get_connection():  #Get connection with database
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('botdata.db', check_same_thread=False)
    return __connection


def init_db(force: bool = False):

    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            user_id         INTEGER NOT NULL, 
            id              INTEGER PRIMARY KEY, 
            text            TEXT NOT NULL
            )
            ''')
    conn.commit()


def add_message(user_id: int, text: str): #Add user message in DB
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?, ?)',
              (user_id, text))
    conn.commit()


def get_random_message(): #Getting random message for users
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT text FROM user_message ORDER BY RANDOM() LIMIT 1',)
    return c.fetchall()


def get_user_message(user_id: int, limit: int = 2): #Getting list of user messages
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT text FROM user_message WHERE user_id = ? ORDER BY id LIMIT ?', (user_id, limit))
    return c.fetchall()
