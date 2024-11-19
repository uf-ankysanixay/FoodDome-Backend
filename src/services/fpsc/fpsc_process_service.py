# src\services\fpsc\fpsc_process_service.py

import os
import json
import pdfplumber
from src.models.fpsc_pod_model import FpscPOD
from src.extensions import db
from sqlalchemy.exc import IntegrityError

def safe_convert(value, value_type):
    """Handles conversion to int or float based on the type passed."""
    try:
        if value_type == "int":
            return int(value.replace(',', '')) if value else None
        elif value_type == "float":
            return float(value.replace('%', '')) if value else None
        else:
            return value
    except ValueError:
        return None

def process_pod(pdf_path, storm_id):
    """Processes the first page of the PDF and returns data for insertion into the FpscPOD table."""
    power_outage_data = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()

        # Ensure there is data to process
        if table and len(table) > 2:
            for row in table[1:-1]:  # Skip the first and last rows
                row = (row + [None] * 19)[:19]  # Ensure we have exactly 19 elements
                if row[0] is None or 'Date/Time' in row[0]:
                    continue

                # Convert row data into a dictionary
                data = {
                    "storm_id": storm_id,
                    "county": row[0].strip() if row[0] else None,
                    "fpl_accounts": safe_convert(row[1], "int") if len(row) > 1 else None,
                    "fpl_out": safe_convert(row[2], "int") if len(row) > 2 else None,
                    "fpl_percentage": safe_convert(row[3], "float") if len(row) > 3 else None,
                    "duke_accounts": safe_convert(row[4], "int") if len(row) > 4 else None,
                    "duke_out": safe_convert(row[5], "int") if len(row) > 5 else None,
                    "duke_percentage": safe_convert(row[6], "float") if len(row) > 6 else None,
                    "tampa_accounts": safe_convert(row[7], "int") if len(row) > 7 else None,
                    "tampa_out": safe_convert(row[8], "int") if len(row) > 8 else None,
                    "tampa_percentage": safe_convert(row[9], "float") if len(row) > 9 else None,
                    "fpu_accounts": safe_convert(row[10], "int") if len(row) > 10 else None,
                    "fpu_out": safe_convert(row[11], "int") if len(row) > 11 else None,
                    "fpu_percentage": safe_convert(row[12], "float") if len(row) > 12 else None,
                    "cooperatives_accounts": safe_convert(row[13], "int") if len(row) > 13 else None,
                    "cooperatives_out": safe_convert(row[14], "int") if len(row) > 14 else None,
                    "cooperatives_percentage": safe_convert(row[15], "float") if len(row) > 15 else None,
                    "municipals_accounts": safe_convert(row[16], "int") if len(row) > 16 else None,
                    "municipals_out": safe_convert(row[17], "int") if len(row) > 17 else None,
                    "municipals_percentage": safe_convert(row[18], "float") if len(row) > 18 else None
                }
                power_outage_data.append(data)

    return power_outage_data

def process_json_and_insert_data_from_filename(filename):
    """Reads the saved JSON file using the storm_id extracted from the filename and inserts data into the database."""
    try:
        # Extract storm_id from the filename by removing the .json extension
        storm_id = filename.rsplit('.', 1)[0]  # This removes the .json extension
        json_filepath = os.path.join("data", "fpsc", filename)

        # Check if the JSON file exists
        if not os.path.exists(json_filepath):
            raise Exception(f"JSON file for {storm_id} does not exist.")

        # Read the JSON data from the file
        with open(json_filepath, 'r') as json_file:
            data = json.load(json_file)

        # Check if the data is an array and process it
        if isinstance(data, list):
            # Insert the data into the database
            result = insert_data_from_json(data)

            return {
                "message": f"Data for storm {storm_id} inserted successfully.",
                "data": result["data"],  # Return the data for confirmation
                "skipped_rows": result["skipped_rows"]  # Return skipped rows
            }

        else:
            raise Exception(f"Invalid JSON structure in {storm_id}. Expected an array of data.")

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        raise Exception(f"Error processing JSON and inserting data: {str(e)}")

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
                # Attempt to add and flush to check for duplicates
                db.session.add(pod_entry)
                db.session.flush()  # Flush the session to detect any duplicate entries

            except IntegrityError as e:
                # If IntegrityError is raised, capture the skipped entry and continue
                db.session.rollback()  # Rollback the session to avoid partial data insertion
                skipped_rows.append(entry)  # Add the skipped entry to skipped_rows
                continue

        # Commit the session if no issues
        db.session.commit()

        # Return the result with skipped rows
        return {
            "message": f"Data inserted successfully. {len(skipped_rows)} duplicates skipped.",
            "skipped_rows": skipped_rows,  # Return the list of skipped rows
            "data": data  # Return the inserted data
        }

    except Exception as e:
        db.session.rollback()  # Rollback in case of any failure
        raise Exception(f"Error inserting data into the database: {str(e)}")
