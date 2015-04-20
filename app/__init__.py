from flask import Flask
from werkzeug.contrib.fixers import LighttpdCGIRootFix, HeaderRewriterFix

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
app.wsgi_app = HeaderRewriterFix(app.wsgi_app, remove_headers=['Date'], add_headers=[('X-Powered-By', 'WSGI'), ('Server', 'Noname Server')])

from app import views
