from flask import Flask, request

from components import bundles, routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bundles.register(app)
routes.register(app, request)
app.run()
