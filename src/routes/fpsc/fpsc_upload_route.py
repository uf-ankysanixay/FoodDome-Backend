import os
from flask import Blueprint, jsonify, request
from datetime import datetime
from src.services.fpsc.fpsc_upload_service import handle_upload

# Define Blueprint
fpsc_upload_bp = Blueprint('fpsc_upload_bp', __name__)

# Route to upload and process PDFs
@fpsc_upload_bp.route('/upload-pdfs', methods=['POST'])
def upload_pdfs():
    try:
        # Log the incoming request details
        print(f"Request Content-Type: {request.content_type}")
        print(f"Request Files: {request.files.keys()}")

        # Check if the request has files
        if 'files' not in request.files:
            return jsonify({"error": "No files part in the request"}), 400

        files = request.files.getlist('files')  # Get all files from the request
        if not files or all(file.filename == '' for file in files):
            return jsonify({"error": "No files selected for upload"}), 400

        # Ensure the directory for /data/fpsc exists
        upload_folder = os.path.join(os.getcwd(), 'data', 'fpsc')
        os.makedirs(upload_folder, exist_ok=True)

        # Define the log file path
        log_file_path = os.path.join(upload_folder, 'upload_log.txt')

        results = []
        json_response = None  # Store the JSON response for the first file

        for i, file in enumerate(files):
            try:
                # Validate file size (optional, adjust as needed)
                max_size_mb = 10
                if file.content_length > max_size_mb * 1024 * 1024:
                    raise Exception(f"File {file.filename} exceeds the size limit of {max_size_mb} MB.")

                # Process each file
                result, status = handle_upload(file, upload_folder)

                # Log each upload
                with open(log_file_path, 'a') as log_file:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_file.write(f"{timestamp} - Uploaded file: {file.filename}\n")

                # Add the result to the list
                results.append(result)

                # Save the JSON response for the first file
                if i == 0:
                    json_response = result

            except Exception as e:
                # Log and add error details for the current file
                results.append({"file": file.filename, "error": str(e)})
                print(f"Error processing file {file.filename}: {e}")

        # Return JSON for the first file and a summary of all uploads
        return jsonify({
            "message": "Files processed successfully",
            "json": json_response,
            "upload_summary": results
        }), 200

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500
