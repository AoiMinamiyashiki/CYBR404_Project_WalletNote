/* ============================
   WalletNote Frontend JS
============================ */

/* ---------- Utility ---------- */
function $(id) {
    return document.getElementById(id);
}

function setUserId(uid) {
    localStorage.setItem("walletnote_uid", uid);
}

function getUserId() {
    return localStorage.getItem("walletnote_uid");
}

function logout() {
    localStorage.removeItem("walletnote_uid");
    location.href = "login.html";
}

/* ============================
   Login (username + password)
============================ */
function login() {
    const username = $("username").value.trim();
    const password = $("password").value.trim();

    if (!username || !password) {
        alert("Username and password are required.");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data && data.id) {
            setUserId(data.id);
            location.href = "dashboard.html";
        } else {
            alert("Login failed. Check username or password.");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Login error.");
    });
}

/* ============================
   Signup (username + email + password)
   → immediate dashboard
============================ */
function signup() {
    const username = $("username").value.trim();
    const email = $("email").value.trim();
    const password = $("password").value.trim();

    if (!username || !email || !password) {
        alert("All fields are required.");
        return;
    }

    fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    })
    .then(res => res.json())
    .then(() => {
        // signup後は即ログイン状態にする
        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data && data.id) {
                setUserId(data.id);
                location.href = "dashboard.html";
            } else {
                alert("Signup succeeded but auto-login failed.");
            }
        });
    })
    .catch(err => {
        console.error(err);
        alert("Signup error.");
    });
}

/* ============================
   Dashboard: Record Save
============================ */
function saveRecord() {
    const uid = getUserId();
    if (!uid) {
        location.href = "login.html";
        return;
    }

    fetch("/record", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: uid,
            date: $("date").value,
            amount: parseFloat($("amount").value),
            category: $("category").value,
            type: $("type").value
        })
    })
    .then(() => {
        loadRecords();
        loadCharts();
    });
}

/* ============================
   Load Records
============================ */
function loadRecords() {
    const uid = getUserId();
    if (!uid) return;

    fetch(`/records/${uid}`)
        .then(res => res.json())
        .then(data => {
            $("result").textContent = JSON.stringify(data, null, 2);
        });
}

/* ============================
   OCR Upload
============================ */
function uploadReceipt() {
    const input = $("receipt");
    if (!input || input.files.length === 0) {
        alert("Select an image.");
        return;
    }

    const formData = new FormData();
    formData.append("image", input.files[0]);

    fetch("/ocr", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.date) $("date").value = data.date;
        if (data.amount) $("amount").value = data.amount;
        if (data.category) $("category").value = data.category;
        alert("OCR completed.");
    });
}

/* ============================
   Charts
============================ */
function loadCharts() {
    const uid = getUserId();
    if (!uid) return;

    $("pieChart").src = `/chart/pie/${uid}?type=expense`;
    $("barChart").src = `/chart/bar/${uid}?type=expense`;
}

/* ============================
   Page Guard
============================ */
document.addEventListener("DOMContentLoaded", () => {
    const page = location.pathname.split("/").pop();
    const uid = getUserId();

    if ((page === "dashboard.html" || page === "setting.html") && !uid) {
        location.href = "login.html";
        return;
    }

    if (page === "dashboard.html" && uid) {
        loadRecords();
        loadCharts();
    }
});
