# app\services\fpsc\fpsc_upload_service.py

import os
import json
from werkzeug.utils import secure_filename
from app.services.fpsc.fpsc_process_service import process_pod

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_upload(file, upload_folder):  # Accepts both file and upload_folder
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)

            # Save the file to the specified folder
            file.save(filepath)

            # Use the filename (without the extension) as the storm_id
            storm_id = filename.split('.')[0]

            # Process the uploaded PDF to extract the necessary data
            processed_data = process_pod(filepath, storm_id)

            # Create the JSON filename and path
            json_filename = f"{storm_id}.json"
            json_filepath = os.path.join(upload_folder, json_filename)

            # Write the processed data to the JSON file
            with open(json_filepath, 'w') as json_file:
                json.dump(processed_data, json_file, indent=4)

            # Read the JSON file and return the contents
            with open(json_filepath, 'r') as json_file:
                json_contents = json.load(json_file)

            return {
                "message": "PDF uploaded and JSON file created successfully",
                "data": json_contents,
                "json_file": json_filename
            }, 200

        except Exception as e:
            raise Exception(f"Error processing the file: {str(e)}")
    else:
        raise Exception("Invalid file format. Only PDFs are allowed.")
