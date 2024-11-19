# app\routes\__init__.py

from app.routes.home.home_routes import home_bp
from app.routes.fpsc import fpsc_bp

def register_blueprints(app):
    # Register the home blueprint
    app.register_blueprint(home_bp, url_prefix='/api/home')
    app.register_blueprint(fpsc_bp, url_prefix='/api/fpsc')
