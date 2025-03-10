from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import os
import time  # Simulating processing time
import base64
from ai import ask_ai_to_create_viz, ask_ai_to_create_dashboard, ask_ai_to_create_dashboard_visualizations
from create_visualization import create_visualization, create_dashboard

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}, r"/uploadDashboard": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')  # Flask looks in the 'templates' folder

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')  # Flask looks in the 'templates' folder

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Flask looks in the 'templates' folder

@app.route("/upload", methods=["POST"])
def upload_visualization():
    if "file" not in request.files:
        return jsonify({"message": "No file part", "success": False}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file", "success": False}), 400

    file_content = file.read()
    encoded_file = base64.b64encode(file_content).decode('utf-8')

    vis_definition = ask_ai_to_create_viz(encoded_file)
    vis_id = create_visualization(vis_definition)
    print(f"Visualization ID: {vis_id}")
    return jsonify({"message": "File uploaded and processed successfully", "success": True, "vis_id": vis_id}), 200

@app.route("/uploadDashboard", methods=["POST"])
def upload_dashboard():
    if "file" not in request.files:
        return jsonify({"message": "No file part", "success": False}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file", "success": False}), 400

    file_content = file.read()
    encoded_file = base64.b64encode(file_content).decode('utf-8')

    vizs = ask_ai_to_create_dashboard_visualizations(encoded_file)
    for viz in vizs:
        create_visualization(str(viz), False)
    dashboard = ask_ai_to_create_dashboard(encoded_file)
    print(dashboard)
    dashboard_id = create_dashboard(dashboard)

    print(f"Dashboard ID: {dashboard_id}")
    return jsonify({"message": "File uploaded and processed successfully", "success": True, "dashboard_id": dashboard_id}), 200

if __name__ == "__main__":
    app.run(port=8000, debug=True)
