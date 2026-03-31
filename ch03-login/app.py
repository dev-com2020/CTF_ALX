#!/usr/bin/env python3
"""
ALX Academy CTF - Challenge 03: Broken Login
Podatnosc: SQL Injection (UNION-based)
Flaga: ALX{sql1_byp4ss_un10n_s3l3ct}
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'ALX{sql1_byp4ss_un10n_s3l3ct}')

# ── Baza danych w pamieci ─────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

DB = get_db()

def init_db():
    DB.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role     TEXT DEFAULT 'user'
        )
    """)
    DB.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id    INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """)
    DB.execute("INSERT INTO users VALUES (1, 'admin', 'Sup3rS3cr3tP4ssw0rd!', 'admin')")
    DB.execute("INSERT INTO users VALUES (2, 'alice', 'alice123', 'user')")
    DB.execute("INSERT INTO users VALUES (3, 'bob',   'qwerty',  'user')")
    DB.execute(f"INSERT INTO secrets VALUES (1, 'flag', '{FLAG}')")
    DB.execute(f"INSERT INTO secrets VALUES (2, 'api_key', 'sk-prod-a8f3k2j9x1')")
    DB.commit()

init_db()

# ── Szablony HTML ──────────────────────────────────────────────────────────
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>TechCorp :: Panel Administracyjny</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Courier New', monospace;
      background: #0d1117;
      color: #c9d1d9;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }
    .container {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 40px;
      width: 420px;
    }
    .logo {
      text-align: center;
      margin-bottom: 30px;
    }
    .logo h1 {
      color: #58a6ff;
      font-size: 1.4em;
      letter-spacing: 3px;
    }
    .logo p {
      color: #8b949e;
      font-size: 0.75em;
      margin-top: 4px;
    }
    label {
      display: block;
      color: #8b949e;
      font-size: 0.8em;
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    input {
      width: 100%;
      padding: 10px 14px;
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 6px;
      color: #c9d1d9;
      font-family: 'Courier New', monospace;
      font-size: 0.9em;
      margin-bottom: 18px;
      outline: none;
    }
    input:focus { border-color: #58a6ff; }
    button {
      width: 100%;
      padding: 11px;
      background: #238636;
      border: 1px solid #2ea043;
      border-radius: 6px;
      color: #fff;
      font-family: 'Courier New', monospace;
      font-size: 0.95em;
      cursor: pointer;
      letter-spacing: 1px;
    }
    button:hover { background: #2ea043; }
    .message {
      margin-top: 20px;
      padding: 12px 16px;
      border-radius: 6px;
      font-size: 0.85em;
      word-break: break-all;
    }
    .error   { background: #2d1215; border: 1px solid #f85149; color: #f85149; }
    .success { background: #0f2d1a; border: 1px solid #2ea043; color: #2ea043; }
    .info    { background: #111d2e; border: 1px solid #58a6ff; color: #58a6ff; }
    .footer {
      margin-top: 24px;
      text-align: center;
      color: #484f58;
      font-size: 0.72em;
    }
    .sql-debug {
      margin-top: 16px;
      padding: 10px 14px;
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 6px;
      font-size: 0.75em;
      color: #8b949e;
      word-break: break-all;
    }
  </style>
</head>
<body>
<div class="container">
  <div class="logo">
    <h1>[ TECHCORP ]</h1>
    <p>Panel Administracyjny v1.2.3</p>
  </div>

  <form method="POST" action="/login">
    <label>Nazwa uzytkownika</label>
    <input type="text" name="username" placeholder="admin" autocomplete="off" value="{{ username }}">
    <label>Haslo</label>
    <input type="password" name="password" placeholder="••••••••">
    <button type="submit">ZALOGUJ SIE</button>
  </form>

  {% if message %}
  <div class="message {{ msg_class }}">{{ message }}</div>
  {% endif %}

  {% if sql_query %}
  <div class="sql-debug">
    <span style="color:#484f58">// wykonane zapytanie:</span><br>
    {{ sql_query }}
  </div>
  {% endif %}

  <div class="footer">
    TechCorp Internal Systems &copy; 2024<br>
    Nieautoryzowany dostep jest zabroniony
  </div>
</div>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>TechCorp :: Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Courier New', monospace;
      background: #0d1117;
      color: #c9d1d9;
      padding: 40px;
    }
    h2 { color: #2ea043; margin-bottom: 20px; }
    .row {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 14px 20px;
      margin-bottom: 10px;
    }
    .key   { color: #8b949e; font-size: 0.8em; }
    .value { color: #58a6ff; margin-top: 4px; word-break: break-all; }
    a { color: #8b949e; font-size: 0.8em; text-decoration: none; }
    a:hover { color: #c9d1d9; }
  </style>
</head>
<body>
  <h2>// Wynik zapytania:</h2>
  {% for row in rows %}
  <div class="row">
    {% for key, val in row.items() %}
    <div class="key">{{ key }}</div>
    <div class="value">{{ val }}</div>
    {% endfor %}
  </div>
  {% endfor %}
  <br><a href="/">&larr; powrot</a>
</body>
</html>
"""

# ── Routes ─────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def index():
    return render_template_string(LOGIN_PAGE,
        message=None, msg_class='', sql_query=None, username='')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # PODATNOSC: bezposrednia interpolacja danych uzytkownika do SQL
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    try:
        rows = DB.execute(query).fetchall()
        rows_as_dicts = [dict(r) for r in rows]

        if rows_as_dicts:
            # Sprawdz czy to normalny login czy payload SQLi
            if len(rows_as_dicts) == 1 and rows_as_dicts[0].get('username') == username:
                msg = f"Witaj, {rows_as_dicts[0]['username']}! Rola: {rows_as_dicts[0]['role']}"
                return render_template_string(LOGIN_PAGE,
                    message=msg, msg_class='success',
                    sql_query=query, username=username)
            else:
                # Wyniki z SQLi - pokaz jak dashboard
                return render_template_string(DASHBOARD_PAGE,
                    rows=rows_as_dicts)
        else:
            return render_template_string(LOGIN_PAGE,
                message='Bledna nazwa uzytkownika lub haslo.',
                msg_class='error', sql_query=query, username=username)

    except Exception as e:
        # Verbose error - ujawnia strukture bazy
        return render_template_string(LOGIN_PAGE,
            message=f'Blad SQL: {e}',
            msg_class='error', sql_query=query, username=username)

@app.route('/robots.txt')
def robots():
    # Easter egg - prowadzacy moze wskazac to uczestnikom jako bonus
    return "User-agent: *\nDisallow: /admin\nDisallow: /backup\n# Tabela: secrets\n", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
