import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from tasks import upload_to_drive

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "✅ Flask + Celery + Redis + Google Drive is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    task = upload_to_drive.delay(file_path, file.filename)
    return jsonify({"task_id": task.id}), 202

@app.route("/status/<task_id>")
def task_status(task_id):
    task = upload_to_drive.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"status": "Processing..."})
    elif task.state == "SUCCESS":
        return jsonify({"status": "Done", "result": task.result})
    else:
        return jsonify({"status": task.state})
