from flask import *
from flask_cors import CORS
import json
from datetime import *
import os 
dailybitz=Flask(__name__)
CORS(dailybitz)
directory= os.path.dirname(os.path.abspath(__file__))
f_name=os.path.join(directory,"users.json")
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
    if username in user:
        if password==user[username]["password"]:
            return jsonify({
                "success":True
            })
        else:
            return jsonify({
                "msg":"Password Incorrect"
            })
    else:
        return jsonify({
            "msg":"User doesn't exist!! Register Now"
        })
    
@dailybitz.route("/add_entries",methods=["POST"])
def entries():
    data=request.json
    username=data.get("username")
    task=data.get("task")
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

@dailybitz.route("/get_entries/<username>")
def get_entries(username):
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
def delete_entry():
    data = request.json
    username = data["username"]
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
def clear_all():
    data = request.json
    username = data["username"]
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

@dailybitz.route("/get_consistency/<username>")
def get_consistency(username):
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

if __name__ == "__main__":
    dailybitz.run()