import sqlite3
from contextlib import contextmanager

from settings import settings


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(settings.DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
