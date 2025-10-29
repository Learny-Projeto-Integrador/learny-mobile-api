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
    
        result, status = login_service.login(validated_data)
        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), status)
        
        access_token = create_access_token(identity=str(result["_id"]))

        return make_response(jsonify(
            access_token=access_token,
            tipo=result.get("tipo"),
            id=result.get("_id"),
            foto=result.get("foto"),
            usuario=result.get("usuario"),
            nome=result.get("nome"),
            email=result.get("email"),
            filhos=result.get("filhos"),
            filhoSelecionado=result.get("filhoSelecionado") or ""
        ), status)
    
api.add_resource(LoginResources, '/login')