from flask import Flask
from config import Configuration

import sys
sys.path.append(r'.\..\..\archiveDecoder') #path for import


app = Flask(__name__)
app.config.from_object(Configuration)
