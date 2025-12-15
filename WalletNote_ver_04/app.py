from flask import Flask, request, jsonify, Response, send_from_directory
from werkzeug.utils import secure_filename
import os

# =========================
# Backend Imports
# =========================
from Backend.Database.CreateDatabase import CreateDatabase
from Backend.Database.RecordDatabase import RecordDatabase
from Backend.Database.RecallDatabase import RecallDatabase
from Backend.System.Login import Login
from Backend.System.Signup import Signup
from Backend.System.OCR_System import OCR_System
from Backend.Information.InputUserInformation import InputUserInformation
from Backend.Chart.MakeChart import MakeChart
from Backend.Chart.CategorySummary import CategorySummary

# =========================
# Flask App Config
# =========================
app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================
# DB Initialization
# =========================
CreateDatabase().create_tables()

# =========================
# Frontend Routing
# =========================
@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/login.html")
def login_page():
    return app.send_static_file("login.html")

@app.route("/signin.html")
def signin_page():
    return app.send_static_file("signin.html")

@app.route("/dashboard.html")
def dashboard_page():
    return app.send_static_file("dashboard.html")

@app.route("/setting.html")
def setting_page():
    return app.send_static_file("setting.html")

# =========================
# Auth API
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({}), 400

    user = Login().authenticate(
        data.get("username"),
        data.get("password")
    )
    return jsonify(user if user else {})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data:
        return {"error": "Invalid data"}, 400

    user = InputUserInformation(
        data.get("username"),
        data.get("email"),
        data.get("password")
    )
    Signup().register(user)

    # signup成功時は成功だけ返す（JS側でauto-login）
    return {"status": "ok"}

# =========================
# Record API
# =========================
@app.route("/record", methods=["POST"])
def record():
    data = request.json
    if not data:
        return {"error": "Invalid data"}, 400

    RecordDatabase().save(
        user_id=data.get("user_id"),
        date=data.get("date"),
        amount=data.get("amount"),
        category=data.get("category"),
        type_=data.get("type")
    )
    return {"status": "saved"}

@app.route("/records/<int:user_id>")
def records(user_id):
    records = RecallDatabase().fetch_by_user(user_id)
    return jsonify(records)

# =========================
# OCR API
# =========================
@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    file = request.files["image"]
    if file.filename == "":
        return {"error": "Empty filename"}, 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    ocr_engine = OCR_System(
        tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    result = ocr_engine.scan_receipt(path)

    return jsonify(result)

# =========================
# Chart API
# =========================
@app.route("/chart/pie/<int:user_id>")
def chart_pie(user_id):
    record_type = request.args.get("type")  # expense / income / None
    records = RecallDatabase().fetch_by_user(user_id)

    summary = CategorySummary().summarize(records, record_type)
    if not summary:
        return {"error": "No data"}, 404

    img = MakeChart().pie(
        summary,
        title=f"Category Share ({record_type or 'all'})"
    )
    return Response(img, mimetype="image/png")

@app.route("/chart/bar/<int:user_id>")
def chart_bar(user_id):
    record_type = request.args.get("type")
    records = RecallDatabase().fetch_by_user(user_id)

    summary = CategorySummary().summarize(records, record_type)
    if not summary:
        return {"error": "No data"}, 404

    img = MakeChart().bar(
        summary,
        title=f"Category Total ({record_type or 'all'})"
    )
    return Response(img, mimetype="image/png")

# =========================
# Uploaded Files (Debug)
# =========================
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
