# Importando a classe Resource do Flask-Restful
from bson import ObjectId
from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.children_schemas import ChildrenSchema, ChildrenLoginSchema
from ..models import database
from ..services import children_service
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class ChildrenResources(Resource):
    @jwt_required()
    def get(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        return make_response(jsonify(children), 200)
    
    def post(self):
        mv = ChildrenSchema()

        try:
            validated_data = mv.load(request.json)
        except ValidationError:
            # Se der erro de validação, responde mensagem única
            return make_response(jsonify({"error": "Preencha todos os campos obrigatórios."}), 400)

        # Se passou na validação:
        foto = validated_data["foto"]
        usuario = validated_data["usuario"]
        senha = validated_data["senha"]
        nome = validated_data["nome"]
        email = validated_data["email"]
        dataNasc = validated_data["dataNasc"]
        responsavel = validated_data["responsavel"]

        new_children = database.Criancas(foto=foto, usuario=usuario, senha=senha, nome=nome, email=email, dataNasc=dataNasc, responsavel=responsavel)
        result = children_service.register_children(new_children)

        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)

        return make_response(jsonify(result["message"]), 201)
        
class ChildrenDetail(Resource):
    @jwt_required()
    def delete(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        if children is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        
        children_service.delete_children(id)
        return make_response(jsonify("Conta excluída com sucesso"), 204)

class ChildrenLoginResources(Resource):
    def post(self):
        mv = ChildrenLoginSchema()
        try:
            validated_data = mv.load(request.json)
        except ValidationError:
            # Se der erro de validação, responde mensagem única
            return make_response(jsonify({"error": "Preencha todos os campos obrigatórios."}), 400)
    
        result = children_service.login_children(validated_data)
        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)
        
        access_token = create_access_token(identity=str(result["_id"]))
        return make_response(jsonify(access_token=access_token), 200)
      
api.add_resource(ChildrenResources, '/criancas')
api.add_resource(ChildrenDetail, '/criancas/<id>')
api.add_resource(ChildrenLoginResources, '/criancas/login')
