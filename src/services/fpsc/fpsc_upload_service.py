import os
import json
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from src.models.fpsc_pod_model import FpscPOD  # Import your database model
from src.extensions import db  # Import SQLAlchemy database session
from src.services.fpsc.fpsc_process_service import process_pod

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE_MB = 10  # Define a maximum file size limit (optional)


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def insert_data_from_json(data):
    """Inserts data into FpscPOD table and tracks skipped entries due to duplicates."""
    skipped_rows = []  # Initialize the list to capture skipped rows

    try:
        for entry in data:
            pod_entry = FpscPOD(
                storm_id=entry.get("storm_id"),
                county=entry.get("county"),
                fpl_accounts=entry.get("fpl_accounts"),
                fpl_out=entry.get("fpl_out"),
                fpl_percentage=entry.get("fpl_percentage"),
                duke_accounts=entry.get("duke_accounts"),
                duke_out=entry.get("duke_out"),
                duke_percentage=entry.get("duke_percentage"),
                tampa_accounts=entry.get("tampa_accounts"),
                tampa_out=entry.get("tampa_out"),
                tampa_percentage=entry.get("tampa_percentage"),
                fpu_accounts=entry.get("fpu_accounts"),
                fpu_out=entry.get("fpu_out"),
                fpu_percentage=entry.get("fpu_percentage"),
                cooperatives_accounts=entry.get("cooperatives_accounts"),
                cooperatives_out=entry.get("cooperatives_out"),
                cooperatives_percentage=entry.get("cooperatives_percentage"),
                municipals_accounts=entry.get("municipals_accounts"),
                municipals_out=entry.get("municipals_out"),
                municipals_percentage=entry.get("municipals_percentage")
            )

            try:
                db.session.add(pod_entry)
                db.session.flush()  # Flush to check for duplicates
            except IntegrityError:
                db.session.rollback()  # Rollback to avoid partial inserts
                skipped_rows.append(entry)  # Log the skipped entry
                continue

        db.session.commit()
        return {
            "message": f"Data inserted successfully. {len(skipped_rows)} duplicates skipped.",
            "skipped_rows": skipped_rows,
            "data": data
        }

    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error inserting data into the database: {str(e)}")


def handle_upload(file, upload_folder):
    """Handles file upload and processing."""
    try:
        # Validate file type
        if not file or not allowed_file(file.filename):
            raise Exception(f"Invalid file format for {file.filename}. Only PDFs are allowed.")

        # Validate file size
        if file.content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise Exception(f"File {file.filename} exceeds the size limit of {MAX_FILE_SIZE_MB} MB.")

        # Secure the filename
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
        print(f"Error in handle_upload: {e}")
        raise Exception(f"Error processing the file {file.filename}: {str(e)}")
