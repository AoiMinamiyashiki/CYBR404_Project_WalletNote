from flask import Flask, request, jsonify, send_from_directory
import os
import tempfile

# Backend imports (flat structure)
from InputInformation import InputInformation
from RecordDB import RecordDB
from RecallDB import RecallDB
from Dashboard import Dashboard
from OCR_System import OCR_System
from CreateDB import CreateDB

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# -------------------------------------------------
# Initial DB setup (safe on every startup)
# -------------------------------------------------
try:
    creator = CreateDB()
    creator.create_tables()
except Exception as e:
    print(f"[DB INIT WARNING] {e}")


# -------------------------------------------------
# Frontend routing
# -------------------------------------------------
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


@app.route("/login")
def login():
    return send_from_directory("../frontend", "login.html")


@app.route("/signup")
def signup():
    return send_from_directory("../frontend", "signup.html")


@app.route("/dashboard-page")
def dashboard_page():
    return send_from_directory("../frontend", "dashboard.html")


# -------------------------------------------------
# API: Manual record
# -------------------------------------------------
@app.route("/api/record", methods=["POST"])
def record_manual():
    data = request.json

    input_info = InputInformation(
        price=data["price"],
        date=data["date"],
        service_or_product=data["service"]
    )

    RecordDB().insert(input_info)

    return jsonify({
        "status": "success",
        "source": "manual"
    })


# -------------------------------------------------
# API: OCR record
# -------------------------------------------------
@app.route("/api/record/ocr", methods=["POST"])
def record_ocr():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required"}), 400

    image_file = request.files["image"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image_path = tmp.name
        image_file.save(image_path)

    try:
        ocr = OCR_System()
        input_info = ocr.image_to_input_information(image_path)
        RecordDB().insert(input_info)

        response = {
            "status": "success",
            "source": "ocr",
            "data": {
                "price": input_info.price,
                "date": input_info.date,
                "service": input_info.service_or_product
            }
        }

    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return jsonify(response), 500

    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

    return jsonify(response)


# -------------------------------------------------
# API: Records
# -------------------------------------------------
@app.route("/api/records", methods=["GET"])
def records():
    return jsonify(RecallDB().fetch_all())


# -------------------------------------------------
# API: Dashboard data
# -------------------------------------------------
@app.route("/api/dashboard", methods=["GET"])
def dashboard_api():
    data = Dashboard().show()
    return jsonify(data)


# -------------------------------------------------
# Run server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
