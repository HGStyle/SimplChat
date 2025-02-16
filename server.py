from flask import Flask, request
from sqlite3 import connect
from flask_socketio import SocketIO
from datetime import datetime
from hmac import new, compare_digest
from hashlib import sha256
from bcrypt import gensalt, hashpw, checkpw
from re import match

app = Flask('SimplChat-API')
socket = SocketIO(app, cors_allowed_origins="*")
db = connect("db.sqlite3", check_same_thread=False)
hmackey = "4NNxygkVPgkcaVQJEzfwfAKnskWWTQcq"

def verifytoken(username, hashpass, token):
    daytimestamp = (datetime.now() - datetime(1970, 1, 1)).days
    return compare_digest(
        new(
            (hmackey + str(daytimestamp)).encode(),
            (username + hashpass).encode(),
            sha256
        ).hexdigest(),
        token
    )

@app.route("/")
def home():
    return {"status": "200", "message": "Server available"}

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if len(username) < 1:
        return {"status": 400, "message": "Username too short"}
    
    if len(username) > 30:
        return {"status": 400, "message": "Username too long"}
    
    if not match(r'^[A-Za-z][A-Za-z0-9_]{1,30}$', username):
        return {"status": 400, "message": "Invalid character inside username"}

    cur = db.cursor()
    cur.execute("SELECT password FROM accounts WHERE username = ?", (username,))
    data = cur.fetchall()

    if not data:
        cur = db.cursor()
        hashpass = hashpw(password.encode(), gensalt()).decode()
        cur.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashpass))
        db.commit()
        cur.close()
    
    else:
        if not checkpw(password.encode(), data[0][0].encode()):
            return {"status": 401, "message": "Incorrect password"}
        hashpass = data[0][0]
    
    daytimestamp = (datetime.now() - datetime(1970, 1, 1)).days
    token = new(
        (hmackey + str(daytimestamp)).encode(),
        (username + hashpass).encode(),
        sha256
    ).hexdigest()

    return {"status": 201, "message": "Token created", "data": token}

@app.route("/check", methods=["POST"])
def check():
    username = request.form.get("username")
    token = request.form.get("token")

    cur = db.cursor()
    cur.execute("SELECT password FROM accounts WHERE username = ?", (username,))
    data = cur.fetchall()

    if not data:
        return {"status": 404, "message": "Account not found"}
    
    if verifytoken(username, data[0][0], token):
        return {"status": 200, "message": "Authentication successful"}
    else:
        return {"status": 403, "message": "Authentication failed"}

@app.route('/channels/list', methods=["POST"])
def list_channels():
    checkresult = check()
    if checkresult["status"] != 200:
        return checkresult

    cur = db.cursor()
    cur.execute("SELECT id, name FROM channels")
    data = cur.fetchall()

    return {
        "status": 200,
        "message": "Channels successfully fetched",
        "data": [{
            "id": channel[0],
            "name": channel[1]
        } for channel in data]
    }

@app.route("/channels/new", methods=["POST"])
def new_channel():
    checkresult = check()
    if checkresult["status"] != 200:
        return checkresult
    
    name = request.form.get("name")
    cur = db.cursor()

    cur.execute("SELECT id FROM channels WHERE name = ? LIMIT 1", (name,))
    data = cur.fetchall()
    if data:
        return {"status": 406, "message": "Channel already exists"}

    cur.execute("INSERT INTO channels (name) VALUES (?)", (name,))
    db.commit()

    cur.execute("SELECT id FROM channels WHERE name = ? LIMIT 1", (name,))
    data = cur.fetchall()
    cur.close()

    return {"status": 201, "message": "Channel created", "data": data[0][0]}

@app.route('/channels/load', methods=["POST"])
def load_channel():
    checkresult = check()
    if checkresult["status"] != 200:
        return checkresult
    
    channel = request.form.get("channel")

    cur = db.cursor()
    cur.execute("SELECT messages.id as id, content, username FROM messages INNER JOIN accounts ON messages.author = accounts.id WHERE channel = ?", (channel,))
    data = cur.fetchall()

    return {
        "status": 200,
        "message": "Messages successfully fetched",
        "data": [{
            "id": message[0],
            "content": message[1],
            "author": message[2]
        } for message in data]
    }

@app.route('/channels/post', methods=["POST"])
def post_in_channel():
    checkresult = check()
    if checkresult["status"] != 200:
        return checkresult
    
    channel = request.form.get("channel")
    content = request.form.get("content")
    username = request.form.get("username")

    cur = db.cursor()
    cur.execute("INSERT INTO messages (content, author, channel) VALUES (?, (SELECT id FROM accounts WHERE username = ?), ?)", (content, username, channel))
    db.commit()
    
    cur.execute('SELECT id FROM messages WHERE content = ? AND author = (SELECT id FROM accounts WHERE username = ?) AND channel = ? ORDER BY id DESC LIMIT 1', (content, username, channel))
    id = cur.fetchone()[0]

    socket.emit("message", {
        "id": id,
        "content": content,
        "author": username,
        "channel": channel
    })

    return {"status": 201, "message": "Message successfully posted"}

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@socket.on('connect')
def handle_connection():
    username = request.args.get("username")
    token = request.args.get("token")

    cur = db.cursor()
    cur.execute("SELECT password FROM accounts WHERE username = ?", (username,))
    data = cur.fetchall()

    if not data:
        return False
    
    if not verifytoken(username, data[0][0], token):
        return False

if __name__ == "__main__":
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, author INTEGER, channel INTEGER)")
    db.commit()
    cur.close()

    socket.run(app, host = '0.0.0.0', port = 5000)