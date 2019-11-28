from flask import Flask
from config import Configuration
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths for import
sys.path.append(os.path.join(BASE_DIR, 'models/oil_carbon_detection/carbon_detection'))
sys.path.append(os.path.join(BASE_DIR, 'models/oil_carbon_detection/oil_detection'))
sys.path.append(os.path.join(BASE_DIR, 'models/ruin-detection'))

app = Flask(__name__)
app.config.from_object(Configuration)
