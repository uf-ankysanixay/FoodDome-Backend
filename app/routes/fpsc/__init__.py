# app\routes\fpsc\__init__.py

from flask import Blueprint

fpsc_bp = Blueprint('fpsc', __name__)

from app.routes.fpsc.fpsc_health_route import fpsc_health_bp
from app.routes.fpsc.fpsc_process_route import fspc_process_bp
from app.routes.fpsc.fpsc_upload_route import fpsc_upload_bp

fpsc_bp.register_blueprint(fpsc_health_bp)
fpsc_bp.register_blueprint(fspc_process_bp)
fpsc_bp.register_blueprint(fpsc_upload_bp)