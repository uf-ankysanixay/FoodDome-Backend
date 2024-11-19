# src\routes\fpsc\fpsc_process_route.py

from flask import Blueprint, jsonify
from src.services.fpsc.fpsc_process_service import process_json_and_insert_data_from_filename

# Define Blueprint
fspc_process_bp = Blueprint('fspc_process_bp', __name__)

# Route to process the JSON file and insert data into the database
@fspc_process_bp.route('/process-json/<filename>', methods=['POST'])
def process_json(filename):
    try:
        # Call the service function to process the JSON and insert data into the database
        result = process_json_and_insert_data_from_filename(filename)

        # Return the result including message, skipped rows, and data
        return jsonify({
            "message": result["message"],
            "skipped_rows": result["skipped_rows"],  # Ensure skipped rows are included
            "data": result["data"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
