from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .serial_controller import init_arduino

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost:27017/learny-bd'
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # chave secreta

init_arduino('COM6')

jwt = JWTManager(app)
ma = Marshmallow(app)

api = Api(app)
mongo = PyMongo(app)

# Importando os recursos
from .resources import parents_resources, children_resources, login_resources, button_resources

