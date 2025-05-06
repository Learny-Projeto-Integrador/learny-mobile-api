# Importando a classe Resource do Flask-Restful
from bson import ObjectId
from flask_restful import Resource
from marshmallow import ValidationError
from api import api
from flask import make_response, jsonify, request
from ..schemas.children_schemas import ChildrenSchema
from ..models import database
from ..services import children_service
from flask_jwt_extended import jwt_required, get_jwt_identity

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

        new_children = database.Criancas(foto=foto, 
                                         usuario=usuario, 
                                         senha=senha, 
                                         nome=nome, 
                                         email=email, 
                                         dataNasc=dataNasc,
                                         pontos=0, 
                                         fasesConcluidas=0,
                                         medalhas=[{}],
                                         rankingAtual=0,
                                         missoesDiarias=[{}],
                                         audio=True,
                                         responsavel=responsavel)
        result = children_service.register_children(new_children)

        if "error" in result:
            return make_response(jsonify({"error": result["error"]}), 400)

        return make_response(jsonify(result["message"]), 201)
        
    @jwt_required()
    def put(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        new_data = request.json
        if children is None:
            return make_response(jsonify("Crianca não encontrada."), 404)
        result = children_service.edit_children(children_id, new_data)
        return make_response(jsonify(result), 200)
    
class ChildrenDetail(Resource):
    @jwt_required()
    def delete(self):
        children_id = get_jwt_identity()
        children = children_service.get_children_by_id(ObjectId(children_id))
        if children is None:
            return make_response(jsonify("Responsável não encontrado."), 404)
        
        children_service.delete_children(id)
        return make_response(jsonify("Conta excluída com sucesso"), 204)

api.add_resource(ChildrenResources, '/criancas')
api.add_resource(ChildrenDetail, '/criancas/<id>')
