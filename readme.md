# DailyBitz 🚀

DailyBitz is a simple and lightweight **productivity tracking web app** that helps users
log their daily tasks, track time spent, and visualize **daily & weekly consistency**
using clean SVG-based progress indicators.

This is my **first full-stack project**, built while learning Flask, JavaScript (fetch),
JSON handling, and deployment.

---

## ✨ Features

- User registration & login
- Add daily tasks with hours spent
- Daily productivity cap (15 hours)
- View today’s task entries
- Delete individual entries or clear all
- Daily & weekly consistency calculation
- Circular SVG progress indicators
- Mobile-responsive UI
- Deployed backend (Flask)

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)
- SVG

### Backend
- Python
- Flask
- Flask-CORS
- JSON (as a lightweight database)

---

## 📁 Project Structure

```text
Dailybitzs/
├── README.md
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── users.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── favicon.jpeg

🌐 Live Backend

The backend is deployed on PythonAnywhere:

https://priyanshumishra0930.pythonanywhere.com


Note: The root (/) URL shows Not Found because this is an API-based backend.
All functionality works via defined endpoints.

⚙️ How It Works

User registers or logs in

Tasks are added with hours (max 15/day)

Backend stores data with date in JSON

Daily & weekly hours are calculated

Consistency is shown using SVG progress rings

⚠️ Disclaimer

DailyBitz caps daily productivity at 15 hours, based on the belief that
continuous all-day productivity is unrealistic and unhealthy.

👨‍💻 Developer

Priyanshu Mishra (Prince)
B.Tech CSE Student
First full-stack project built with Flask 🚀

📌 Notes

This project is built for learning and personal use

Not intended for production-scale usage

Data is stored locally using JSON

📜 License

This project is open for learning and personal experimentation.