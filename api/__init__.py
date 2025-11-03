from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "https://dashboard-learny.vercel.app/"])

# Configurações do banco de dados com variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if DB_USER and DB_PASSWORD:
    mongo_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?retryWrites=true&w=majority"
else:
    mongo_uri = f"mongodb://localhost:27017/{DB_NAME}"

app.config["MONGO_URI"] = mongo_uri
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # chave secreta

jwt = JWTManager(app)
ma = Marshmallow(app)

api = Api(app)
mongo = PyMongo(app)

# Importando os recursos
from .resources import parents_resources, children_resources, login_resources

