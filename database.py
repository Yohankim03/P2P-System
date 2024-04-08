import sqlite3

# Database Initialization
def initialize_database():
    with sqlite3.connect('p2p_messaging.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            port INTEGER
                          );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY,
                            sender_username TEXT,
                            receiver_username TEXT,
                            content TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          );''')
        conn.commit()


# Inserting a New User
def insert_user(username):
    with sqlite3.connect('p2p_messaging.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()

# Saving a Message
def save_message(sender_username, receiver_username, content):
    with sqlite3.connect('p2p_messaging.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (sender_username,))
        sender_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (receiver_username,))
        receiver_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
                       (sender_id, receiver_id, content))
        conn.commit()

# Retrieving Message History for a User
def get_message_history_for_user(username):
    with sqlite3.connect('p2p_messaging.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT m.content, m.timestamp, s.username AS sender, r.username AS receiver
                          FROM messages m
                          JOIN users s ON m.sender_id = s.id
                          JOIN users r ON m.receiver_id = r.id
                          WHERE s.username = ? OR r.username = ?
                          ORDER BY m.timestamp''', (username, username))
        return cursor.fetchall()

# Main Function to Run Some Tests
def main():
    initialize_database()
    insert_user('alice')
    insert_user('bob')

    save_message('alice', 'bob', 'Hello, Bob!')
    save_message('bob', 'alice', 'Hi, Alice!')

    history = get_message_history_for_user('alice')
    for message in history:
        print(message)

if __name__ == '__main__':
    main()
