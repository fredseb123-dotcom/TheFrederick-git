"""
Práce s ticket databází
"""

import sqlite3


def write_data(channel_id: int, member_id: int):
    """Zápis dat o ticketu"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO tickets VALUES ('{channel_id}', '{member_id}')""")
    conn.commit()
    conn.close()


def has_ticket(member_id: int):
    """Check, zda je ID v DB"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tickets WHERE member_id={member_id}""")
    conn.commit()

    if not cursor.fetchone():
        conn.close()
        return False
    conn.close()
    return True


def delete_by_id(member_id: int):
    "Smazání dat dle ID"

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM tickets WHERE member_id={member_id}""")
    conn.commit()
    conn.close()


def is_ticket(channel_id: int):
    """Check, jestli je channel ticketem"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tickets WHERE channel_id={channel_id}""")
    conn.commit()

    if not cursor.fetchone():
        conn.close()
        return False
    conn.close()
    return True


def get_ticket(member_id: int):
    """Získání ID channelu dle autora ticketu"""

    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM tickets WHERE member_id={member_id}""")
    conn.commit()

    return cursor.fetchone()
