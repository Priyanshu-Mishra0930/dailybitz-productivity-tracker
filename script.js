const disclaimer = document.getElementById("disclaimer");
const acceptBtn = document.getElementById("acceptBtn");

if (sessionStorage.getItem("disclaimerAccepted") === "true") {
    disclaimer.style.display = "none";
} else {
    disclaimer.style.display = "flex"; 
}

acceptBtn.addEventListener("click", () => {
    sessionStorage.setItem("disclaimerAccepted", "true");
    disclaimer.style.display = "none";
});


const loginbtn=document.getElementById("log")
const registerbtn=document.getElementById("register")
const authdiv=document.getElementById("auth")
const appdiv=document.getElementById("app")
registerbtn.addEventListener("click",()=>{
    const error_msg=document.getElementById("error")
    const user=document.getElementById("u_id").value.trim();
    const pass=document.getElementById("u_pass").value.trim();
    if (user==="" && pass===""){
        error_msg.innerHTML="Enter User ID and Password!!"
        return;
    }
    fetch("https://priyanshumishra0930.pythonanywhere.com/register",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            username:user,
            password:pass
        })
    })
    .then(res => res.json())
    .then(data => {
        error_msg.innerHTML = data.msg;
        if (data.msg ==="user register succesfully!!"){
            localStorage.setItem("current_user",user);
            authdiv.style.display="none";
            appdiv.style.display="block";
        }
    })
    .catch(err => {
        error_msg.innerHTML = "Server error. Try again.";
    });
});
loginbtn.addEventListener("click",()=>{
    const error_msg=document.getElementById("error")
    const user=document.getElementById("u_id").value.trim();
    const pass=document.getElementById("u_pass").value.trim();
    if (user==="" && pass===""){
        error_msg.innerHTML="Enter User ID and Password!!"
        return;
    }
    fetch("https://priyanshumishra0930.pythonanywhere.com/login",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            username:user,
            password:pass
        })
    })
    .then(res=>res.json())
    .then(data=>{
        error_msg.innerHTML = data.msg;
        if (data.success){
            localStorage.setItem("current_user",user);
            authdiv.style.display="none";
            appdiv.style.display="block";
        }
    })
})
const saved=localStorage.getItem("current_user")
if (saved){
    authdiv.style.display="none"
    appdiv.style.display="block"
    writelist();
}

const logout_user = document.getElementById("delete_data");
logout_user.addEventListener("click", () => {
    const sure = confirm("Do you want to log out?");
    const error_msg=document.getElementById("error");
    
    if (!sure) return;
    localStorage.removeItem("current_user");
    appdiv.style.display = "none";
    authdiv.style.display = "block";
    document.getElementById("u_id").value = "";
    document.getElementById("u_pass").value = "";
    error_msg.innerHTML=" "
});

const add_btn=document.getElementById("add")
add_btn.addEventListener("click", (e)=> {
    e.preventDefault();
    const task=document.getElementById("task").value.trim();
    const hours=parseFloat(document.getElementById("hours").value);
    const added=document.getElementById("msg1")
    
    if (task==="" || isNaN(hours)){
        showMsg("Please enter all fields!!","red")
        return;
    }
    else if (hours<=0){
        showMsg("Hour should be greater than 0!!","red")
        return;
    }
    else if (hours>15){
        showMsg("More than 15 hours is not allowed.!!","red")
        return;
    }
    else{
        const username=localStorage.getItem("current_user")
        add_btn.disabled=true
        fetch("https://priyanshumishra0930.pythonanywhere.com/add_entries",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username:username,
                task:task,
                hours:hours
            })
        })
        .then(res=>res.json())
        .then(data=>{
            if (!localStorage.getItem("current_user")) return;

            showMsg("Entry appended successfully!!");
            document.getElementById("task").value="";
            document.getElementById("hours").value="";
            writelist();
        })
        .finally(()=>{
            add_btn.disabled=false;
        })
}
})
function getdata() {
    const username = localStorage.getItem("current_user");
    return fetch(`https://priyanshumishra0930.pythonanywhere.com/get_entries/${username}`)
        .then(res => res.json());
}

function writelist() {
    if (!localStorage.getItem("current_user")) return;

    const list = document.getElementById("list");
    list.innerHTML = "";

    getdata().then(data => {
        if (!localStorage.getItem("current_user")) return;
        data.forEach((item, index) => {
            const li = document.createElement("li");
            li.innerHTML = `${item.Task} — ${item.Hours} hrs &ensp;
                <button class="del-item" onclick="clear_entry(${index})">x</button>`;
            list.appendChild(li);
        });
    });
}

function clear_entry(index) {
    const username = localStorage.getItem("current_user");
    fetch(`https://priyanshumishra0930.pythonanywhere.com/delete_entry`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            index: index
        })
    })
    .then(res => res.json())
    .then(data => {
        writelist();
    });
}

const clear_data = document.getElementById("clear_all");
clear_data.addEventListener("click", () => {
    const added = document.getElementById("msg1");
    const username = localStorage.getItem("current_user");
    const confirmation = confirm("Are you sure to clear all entries from the database?!!");
    if (!confirmation) return;
    fetch("https://priyanshumishra0930.pythonanywhere.com/clear_all", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username })
    })
    .then(res => res.json())
    .then(data => {
        showMsg(data.msg,data.color)
        writelist();
    });
});

const RADIUS = 50;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

document.querySelectorAll(".progress-ring").forEach(ring => {
    const progress = ring.querySelector(".progress");
    progress.style.strokeDasharray = CIRCUMFERENCE;
    progress.style.strokeDashoffset = CIRCUMFERENCE;
});

function setProgress(ring, percent) {
    percent = Math.max(0, Math.min(100, percent));
    const offset = CIRCUMFERENCE - (percent / 100) * CIRCUMFERENCE;

    ring.querySelector(".progress").style.strokeDashoffset = offset;
    ring.querySelector(".percent").textContent = percent.toFixed(1) + "%";
}

const consistency=document.getElementById("consi_btn")
consistency.addEventListener("click", () => {
    const username=localStorage.getItem("current_user");

    fetch(`https://priyanshumishra0930.pythonanywhere.com/get_consistency/${username}`)
        .then(res=>res.json())
        .then(data => {
            if (!localStorage.getItem("current_user")) return;

            const daily = data.daily;
            const weekly = data.weekly;

            if (isNaN(daily) || isNaN(weekly)) {
                showMsg("Oops!! looks like you don't have any entries", "red");
                document.getElementById("greeting").textContent = "";
                return;
            }

            if (daily === 0 && weekly === 0) {
                showMsg("No data Available!!", "red");
                document.getElementById("greeting").textContent = "";
                return;
            }

            document.querySelectorAll(".progress-ring").forEach(ring => {
                const type = ring.dataset.type;

                if (type === "daily") setProgress(ring, daily);
                if (type === "weekly") setProgress(ring, weekly);
            });

            document.getElementById("greeting").textContent = "Keep going buddy!!🔥";
        });
});

function showMsg(text, color="#2e7d32"){
    const added = document.getElementById("msg1");
    added.textContent = text;
    added.style.color = color;

    setTimeout(() => {
        added.textContent = "";
    }, 2500);
}