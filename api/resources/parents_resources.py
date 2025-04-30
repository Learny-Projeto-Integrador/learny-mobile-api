# Importando a classe Resource do Flask-Restful
from bson import ObjectId
from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.parent_schemas import ParentSchema, ParentLoginSchema
from ..models import database
from ..services import parent_service
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class ParentResources(Resource):
    @jwt_required()
    def get(self):
        parent_id = get_jwt_identity()
        parent = parent_service.get_parent_by_id(ObjectId(parent_id))
        return make_response(jsonify(parent), 200)
    
    def post(self):
        mv = ParentSchema()

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

        new_parent = database.Pais(foto=foto, usuario=usuario, senha=senha, nome=nome, email=email, dataNasc=dataNasc, filhos=[], filhoSelecionado={})
        result = parent_service.register_parent(new_parent)

        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)

        return make_response(jsonify(result["message"]), 201)

    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()
        parent = parent_service.get_parent_by_id(ObjectId(parent_id))
        new_data = request.json
        if parent is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        parent_service.edit_parent(parent_id, new_data)
        return make_response(jsonify(parent), 200)
        
    @jwt_required()
    def delete(self):
        parent_id = get_jwt_identity()
        parent = parent_service.get_parent_by_id(ObjectId(parent_id))
        if parent is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        
        parent_service.delete_parent(id)
        return make_response(jsonify("Conta excluída com sucesso"), 204)

class ParentLoginResources(Resource):
    def post(self):
        mv = ParentLoginSchema()
        try:
            validated_data = mv.load(request.json)
        except ValidationError:
            # Se der erro de validação, responde mensagem única
            return make_response(jsonify({"error": "Preencha todos os campos obrigatórios."}), 400)
    
        result = parent_service.login_parent(validated_data)
        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)
        
        access_token = create_access_token(identity=str(result["_id"]))
        return make_response(jsonify(access_token=access_token), 200)
    
class AddChildrenResources(Resource):
    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()
        parent = parent_service.get_parent_by_id(ObjectId(parent_id))
        new_children = request.json
        if parent is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        parent_service.add_children(parent_id, new_children)
        return make_response(jsonify(parent), 200)
    
class EditSelectedChildrenResources(Resource):
    @jwt_required()
    def put(self):
        parent_id = get_jwt_identity()
        parent = parent_service.get_parent_by_id(ObjectId(parent_id))
        new_children = request.json
        if parent is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        parent_service.edit_selected_children(parent_id, new_children)
        return make_response(jsonify(parent), 200)

      
api.add_resource(ParentResources, '/pais')
api.add_resource(ParentLoginResources, '/pais/login')
api.add_resource(AddChildrenResources, '/pais/addcrianca')
api.add_resource(EditSelectedChildrenResources, '/pais/filhoselecionado')
