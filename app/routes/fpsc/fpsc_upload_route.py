# app\routes\fpsc\fpsc_upload_route.py

import os
from flask import Blueprint, jsonify, request
from app.services.fpsc.fpsc_upload_service import handle_upload

# Define Blueprint
fpsc_upload_bp = Blueprint('fpsc_upload_bp', __name__)

# Route to upload and process PDF
@fpsc_upload_bp.route('/upload-pdfs', methods=['POST'])
def upload_pdf():
    # Check if the file part exists in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if a file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Ensure the directory for /data/fpsc exists
        upload_folder = os.path.join(os.getcwd(), 'data', 'fpsc')
        os.makedirs(upload_folder, exist_ok=True)

        # Call the service to handle the upload and return the result (including the JSON data)
        result = handle_upload(file, upload_folder)  # Pass both the file and the upload folder

        # If the file was uploaded and the JSON was created successfully, return the result
        return jsonify(result), 200  # Return the result which includes the JSON data

    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 500
