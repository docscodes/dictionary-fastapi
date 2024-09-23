import sqlite3 as SQL


def match_exact(word: str) -> list:
  db = SQL.connect("data/dictionary.db")
  sql_query = "SELECT * from entries WHERE word=?"

  match = db.execute(sql_query, (word,)).fetchall()
  db.close()

  return match


def match_like(word: str) -> list:
  db = SQL.connect("data/dictionary.db")
  sql_query = "SELECT * from entries WHERE word LIKE ?"

  match = db.execute(sql_query, ("%" + word + "%",)).fetchall()
  db.close()

  return match
