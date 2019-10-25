from flask import Flask
from config import Configuration
import sys

sys.path.append(r'.\..\..\oil-carbon-detection\oil-detection')
sys.path.append(r'.\..\..\ruin-detection')

app = Flask(__name__)
app.config.from_object(Configuration)
