from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os
from config import *
from utils.image_crop import crop_image

app = Flask(__name__)
CORS(app)

# ---------------- MongoDB ----------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ---------------- Upload Folders ----------------
os.makedirs(PROJECT_FOLDER, exist_ok=True)
os.makedirs(CLIENT_FOLDER, exist_ok=True)

# ---------------- Home Pages ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

# ---------------- Serve Uploaded Images ----------------
@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory("uploads", filename)

# ---------------- Projects API ----------------
@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("name")
        desc = request.form.get("description")

        if not image or not name:
            return jsonify({"error": "Missing data"}), 400

        image_path = os.path.join(PROJECT_FOLDER, image.filename)
        image.save(image_path)
        crop_image(image_path, image_path)

        db.projects.insert_one({
            "name": name,
            "description": desc,
            "image": f"/uploads/projects/{image.filename}"
        })

        return jsonify({"msg": "Project added successfully"})

    projects = list(db.projects.find({}, {"_id": 0}))
    return jsonify(projects)

# ---------------- Clients API ----------------
@app.route("/clients", methods=["GET", "POST"])
def clients():
    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("name")
        desc = request.form.get("description")
        designation = request.form.get("designation")

        if not image or not name:
            return jsonify({"error": "Missing data"}), 400

        image_path = os.path.join(CLIENT_FOLDER, image.filename)
        image.save(image_path)
        crop_image(image_path, image_path)

        db.clients.insert_one({
            "name": name,
            "description": desc,
            "designation": designation,
            "image": f"/uploads/clients/{image.filename}"
        })

        return jsonify({"msg": "Client added successfully"})

    clients = list(db.clients.find({}, {"_id": 0}))
    return jsonify(clients)

# ---------------- Contact API ----------------
@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        db.contacts.insert_one(request.json)
        return jsonify({"msg": "Contact saved"})

    contacts = list(db.contacts.find({}, {"_id": 0}))
    return jsonify(contacts)

# ---------------- Newsletter API ----------------
@app.route("/subscribe", methods=["POST", "GET"])
def subscribe():
    if request.method == "POST":
        db.subscribers.insert_one(request.json)
        return jsonify({"msg": "Subscribed successfully"})

    subs = list(db.subscribers.find({}, {"_id": 0}))
    return jsonify(subs)

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)
