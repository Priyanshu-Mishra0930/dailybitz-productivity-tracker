from flask import *
from flask_cors import CORS
import json
from datetime import *
import os
import html
import secrets
from functools import wraps
dailybitz=Flask(__name__)
CORS(dailybitz)
directory= os.path.dirname(os.path.abspath(__file__))
f_name=os.path.join(directory,"users.json")
active_tokens = {}
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json(silent=True) or {}
        token = data.get("token")

        if not token or token not in active_tokens:
            return jsonify({"msg": "Unauthorized"}), 401

        token_data = active_tokens[token]

        if datetime.utcnow() > token_data["expires"]:
            del active_tokens[token]
            return jsonify({"msg": "Session expired. Please login again."}), 401

        request.username = token_data["username"]
        return f(*args, **kwargs)
    return decorated


def read():
    if not os.path.exists(f_name):
        return {}
    try:
        with open(f_name, "r") as f:
            return json.load(f)
    except:
        return {}

def write(tasks):
    with open (f_name,"w") as f:
        json.dump(tasks,f,indent=2)

@dailybitz.route("/register",methods=["POST"])
def add_user():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    if not username or not password:
        return jsonify({
            "msg":"Enter User ID and Password!!"
        }),400
    user=read()
    if username in user:
        return jsonify({
            "msg":"Username already exists! Try another name."
        }),409
    if not password or len(password)<4:
        return jsonify({
            "msg":"Password must be of 4 or more digits!!"
        }),409
    user[username]={
        "password":password,
        "entries":[]
    }
    write(user)
    return jsonify({
        "msg":"User registered successfully!!"
    })

@dailybitz.route("/login",methods=["POST"])
def added_user():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    if not username or not password:
        return jsonify({
            "msg":"Enter User ID and Password!!"
        }),400
    user=read()
    if username in user and password==user[username]["password"]:
        token = secrets.token_hex(16)
        active_tokens[token] = {
            "username":username,
            "expires":datetime.utcnow() + timedelta(hours=6)
            }
        return jsonify({
            "success":True,
            "token":token
        })
    else:
        return jsonify({
            "msg":"Invalid credentials"
        }),401

@dailybitz.route("/add_entries",methods=["POST"])
@token_required
def entries():
    data=request.json
    username=request.username
    task=data.get("task")
    task=html.escape(task)
    try:
        hours = float(data.get("hours"))
        if hours <= 0 or hours > 15:
            raise ValueError
    except:
        return jsonify({"msg": "Invalid hours"}), 400
    user=read()
    if username not in user:
        return jsonify({"msg": "Invalid user"}), 400

    user[username]["entries"].append({
        "Task":task,
        "Hours":hours,
        "Date":date.today().isoformat()
    })
    write(user)
    return jsonify({
        "msg":"Entry appended Successfully!!"
    })

@dailybitz.route("/get_entries",methods=["POST"])
@token_required
def get_entries():
    username=request.username
    users = read()

    if username not in users:
        return jsonify([])
    today=date.today().isoformat()

    today_entries=[]
    e=users[username]["entries"]
    for i in e :
        if i["Date"]==today:
            today_entries.append(i)
    return jsonify(today_entries)


@dailybitz.route("/delete_entry", methods=["DELETE"])
@token_required
def delete_entry():
    data = request.json
    username = request.username
    index = data["index"]
    users = read()
    if username not in users:
        return jsonify({"msg": "Invalid user"}), 400

    entries = users[username]["entries"]
    if index < 0 or index >= len(entries):
        return jsonify({"msg": "Invalid index"}), 400
    entries.pop(index)

    write(users)
    return jsonify({"msg": "Entry deleted"})

@dailybitz.route("/clear_all", methods=["DELETE"])
@token_required
def clear_all():
    data = request.json
    username = request.username
    users = read()
    if username not in users:
        return jsonify({"msg": "Invalid user"}), 400

    if users[username]["entries"] == []:
        return jsonify({
        "msg": "No entries available to clear.!!",
        "color":"red"
    })

    users[username]["entries"] = []
    write(users)
    return jsonify({
        "msg": "All entries cleared",
        "color":"#2e7d32"
    })

@dailybitz.route("/get_consistency",methods=["POST"])
@token_required
def get_consistency():
    username=request.username
    users=read()
    if username not in users:
        return jsonify({"msg": "User not found"}),404
    entries=users[username]["entries"]
    if entries==[]:
        return jsonify({"msg":"No entries yet."}),404

    today=date.today()
    week_star=today-timedelta(days=6)

    daily=0
    weekly=0

    for e in entries:
        entry_date=date.fromisoformat(e["Date"])
        hours=e["Hours"]
        if entry_date==today:
            daily+=hours
        if week_star<=entry_date<=today:
            weekly+=hours
    daily_consistency=round((daily/15)*100,2)
    weekly_consistency=round((weekly/105)*100,2)

    return jsonify({
        "daily":daily_consistency,
        "weekly":weekly_consistency
    })
