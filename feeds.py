import sqlite3
import sys
import feedparser
from datetime import datetime

DATABASE = 'feeds.sqlite'

class Entry(object): pass

class Feeds(object):

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        """create tables if they don't already exist"""
        c.execute('CREATE TABLE IF NOT EXISTS feeds (feed_id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000));')
        c.execute('CREATE TABLE IF NOT EXISTS entries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, feed_id INTEGER, id INTEGER, link VARCHAR(1000), title VARCHAR(1000), summary TEXT, published DATETIME, updated DATETIME);')
        c.close()

    def _process_entries(self, feed_id, entries):
        c = self.conn.cursor()
        new = 0
        seen = 0
        for entry in entries:
            c.execute('SELECT * FROM entries WHERE feed_id = ? AND id = ?', (feed_id, entry.id))
            if len(c.fetchall()) == 0:
                new = new + 1
                c.execute('INSERT INTO entries (feed_id, id, link, title, summary, published, updated) VALUES (?, ?,?,?,?,?,?)', (feed_id, entry.id, entry.link, entry.title, entry.summary, datetime(*entry.published_parsed[:6]), datetime(*entry.updated_parsed[:6])))
            else:
                seen = seen + 1
        c.close()
        self._commit()
        return (new, seen)

    def _commit(self):
        self.conn.commit()

    def _get_feed_id(self, feed_url):
        c = self.conn.cursor()
        c.execute('SELECT feed_id FROM feeds WHERE url = ?', (feed_url,))
        row = c.fetchone()
        if row:
            feed_id = row[0]
        else:
            c.execute('INSERT INTO feeds (url) VALUES (?)', (feed_url,))
            feed_id = c.lastrowid
            self._commit()
        c.close()
        return feed_id

    def _make_entry(self, cursor, row):
        e = Entry()
        for idx, col in enumerate(cursor.description):
            setattr(e, col[0], row[idx])
        return e

    def update(self, feed_url):
        entries = feedparser.parse(feed_url).entries
        feed_id = self._get_feed_id(feed_url)
        counts = self._process_entries(feed_id, entries)
        return counts

    def get_recent(self, feed_url, n = 5, pattern = None):
        feed_id = self._get_feed_id(feed_url)
        c = self.conn.cursor()
        if pattern:
            c.execute('SELECT * FROM entries WHERE feed_id = ? AND title LIKE ? ' + \
                    'ORDER BY published DESC LIMIT ?', (feed_id, pattern, n))
        else:
            c.execute('SELECT * FROM entries WHERE feed_id = ? ORDER BY published DESC LIMIT ?', (feed_id, n))
        recent = [self._make_entry(c, row) for row in c.fetchall()]
        c.close()
        return recent

    def close(self):
        self.conn.close()
