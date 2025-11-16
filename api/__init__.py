from flask import Flask, jsonify
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
import os
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    RevokedTokenError,
    UserLookupError,
    WrongTokenError,
    FreshTokenRequired,
    CSRFError
)
from jwt.exceptions import ExpiredSignatureError

class CustomApi(Api):
    def handle_error(self, e):
        if isinstance(e, NoAuthorizationError):
            return jsonify({"msg": "Token de autenticação ausente ou inválido."}), 401
        if isinstance(e, InvalidHeaderError):
            return jsonify({"msg": "Cabeçalho JWT inválido."}), 422
        if isinstance(e, ExpiredSignatureError):
            return jsonify({"msg": "Token expirado."}), 401
        if isinstance(e, RevokedTokenError):
            return jsonify({"msg": "Token revogado."}), 401
        if isinstance(e, UserLookupError):
            return jsonify({"msg": "Usuário associado ao token não encontrado."}), 401
        if isinstance(e, WrongTokenError):
            return jsonify({"msg": "Tipo de token incorreto para esta operação."}), 422
        if isinstance(e, FreshTokenRequired):
            return jsonify({"msg": "Token 'fresh' é necessário para esta operação."}), 401
        if isinstance(e, CSRFError):
            return jsonify({"msg": "Erro de verificação CSRF."}), 401
        return super().handle_error(e)

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
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default-secret")

jwt = JWTManager(app)
ma = Marshmallow(app)

api = CustomApi(app)
mongo = PyMongo(app)

# Importando os recursos
from .resources import parents_resources, children_resources, login_resources

