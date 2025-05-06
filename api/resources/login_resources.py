from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.login_schemas import LoginSchema
from ..services import login_service
from flask_jwt_extended import create_access_token

class LoginResources(Resource):
    def post(self):
        mv = LoginSchema()
        try:
            validated_data = mv.load(request.json)
        except ValidationError:
            # Se der erro de validação, responde mensagem única
            return make_response(jsonify({"error": "Preencha todos os campos obrigatórios."}), 400)
    
        result = login_service.login(validated_data)
        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)
        
        access_token = create_access_token(identity=str(result["_id"]))
        tipo_usuario = result.get("tipo")
        nome_usuario = result.get("nome")

        return make_response(jsonify(
            access_token=access_token,
            tipo=tipo_usuario,
            nome=nome_usuario
        ), 200)
    
api.add_resource(LoginResources, '/login')