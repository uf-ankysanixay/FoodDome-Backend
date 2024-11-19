# src\routes\fpsc\fpsc_health_route.py

from flask import Blueprint, jsonify

# Define Blueprint for FPSC health check
fpsc_health_bp = Blueprint('fpsc_health', __name__)

@fpsc_health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "FPSC service is running.",
        "data": {}
    }), 200
