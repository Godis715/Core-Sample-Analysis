from flask import Flask
from config import Configuration
import logging
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths for import
sys.path.append(os.path.join(BASE_DIR, 'models/oil_carbon_detection/carbon_detection'))
sys.path.append(os.path.join(BASE_DIR, 'models/oil_carbon_detection/oil_detection'))
sys.path.append(os.path.join(BASE_DIR, 'models/ruin-detection'))
sys.path.append(os.path.join(BASE_DIR, 'models/rock_classification'))

def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/analyse-api.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('ANALYSE-API startup')

    return app